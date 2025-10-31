import tempfile
from pathlib import Path
import shutil
import subprocess
import time

class MLIRLoweringPipeline:

    def __init__(self):
        self.verify_tools()

    def verify_tools(self):
        """Verify required MLIR tools"""
        required_tools = ['mlir-opt', 'mlir-translate']
        for tool in required_tools:
            if not shutil.which(tool):
                raise RuntimeError(f'Required tool not found: {tool}')
        print('✅ MLIR tools verified: mlir-opt, mlir-translate')

    def find_available_passes(self):
        """Find what lowering passes are available"""
        print('🔍 Finding available lowering passes...')
        try:
            result = subprocess.run(['mlir-opt', '--help'], capture_output=True, text=True)
            help_text = result.stdout
            conversion_passes = []
            for line in help_text.splitlines():
                line = line.strip()
                if 'convert-' in line and '-to-' in line:
                    if line.startswith('--'):
                        pass_name = line.split()[0][2:]
                        conversion_passes.append(pass_name)
            print('📋 Available conversion passes:')
            relevant_passes = []
            for pass_name in sorted(conversion_passes):
                if any((keyword in pass_name for keyword in ['arith', 'func', 'llvm', 'std', 'scf'])):
                    print(f'   ✅ {pass_name}')
                    relevant_passes.append(pass_name)
                else:
                    print(f'   ❓ {pass_name}')
            return relevant_passes
        except Exception as e:
            print(f'❌ Error finding passes: {e}')
            return []

    def test_lowering_passes(self, input_file):
        """Test different lowering pass combinations"""
        print(f'\n🧪 Testing lowering passes on {input_file}...')
        pass_sequences = [['convert-arith-to-llvm'], ['convert-arith-to-llvm', 'convert-func-to-llvm'], ['convert-arith-to-llvm', 'convert-func-to-llvm', 'convert-scf-to-cf', 'convert-cf-to-llvm'], ['arith-bufferize', 'convert-arith-to-llvm'], ['canonicalize', 'convert-arith-to-llvm', 'canonicalize'], ['convert-arith-to-llvm', 'convert-func-to-llvm', 'reconcile-unrealized-casts']]
        successful_sequences = []
        for i, passes in enumerate(pass_sequences):
            print(f"\n📋 Testing sequence {i + 1}: {' → '.join(passes)}")
            success = self.test_pass_sequence(input_file, passes)
            if success:
                successful_sequences.append(passes)
                print(f'   ✅ Sequence {i + 1} works!')
            else:
                print(f'   ❌ Sequence {i + 1} failed')
        return successful_sequences

    def test_pass_sequence(self, input_file, passes):
        """Test a specific sequence of passes"""
        try:
            pipeline = f"builtin.module({','.join(passes)})"
            with tempfile.NamedTemporaryFile(suffix='.mlir', delete=False) as temp_file:
                cmd = ['mlir-opt', input_file, f'--pass-pipeline={pipeline}']
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
                if result.returncode != 0:
                    return False
                temp_file.write(result.stdout)
                temp_file.flush()
                cmd = ['mlir-translate', '--mlir-to-llvmir', temp_file.name]
                translate_result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                success = translate_result.returncode == 0
                if success:
                    print(f'      💡 LLVM IR size: {len(translate_result.stdout)} chars')
                return success
        except Exception as e:
            print(f'      ❌ Error: {e}')
            return False
        finally:
            try:
                Path(temp_file.name).unlink()
            except:
                pass

    def create_lowered_file(self, input_file, output_file, pass_sequence):
        """Create a fully lowered MLIR file"""
        print(f'\n🚀 Creating lowered file: {input_file} → {output_file}')
        print(f"📋 Using passes: {' → '.join(pass_sequence)}")
        try:
            pipeline = f"builtin.module({','.join(pass_sequence)})"
            start_time = time.time()
            cmd = ['mlir-opt', input_file, f'--pass-pipeline={pipeline}', '-o', output_file]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            elapsed = time.time() - start_time
            if result.returncode != 0:
                print(f'❌ Lowering failed: {result.stderr}')
                return False
            print(f'✅ Lowering completed in {elapsed:.3f}s')
            output_path = Path(output_file)
            if output_path.exists():
                size = output_path.stat().st_size
                print(f'📄 Output file size: {size} bytes')
                cmd = ['mlir-translate', '--mlir-to-llvmir', output_file]
                translate_result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
                if translate_result.returncode == 0:
                    llvm_size = len(translate_result.stdout)
                    print(f'✅ LLVM translation successful! LLVM IR size: {llvm_size} chars')
                    llvm_file = output_file.replace('.mlir', '.ll')
                    with open(llvm_file, 'w') as f:
                        f.write(translate_result.stdout)
                    print(f'💾 LLVM IR saved to: {llvm_file}')
                    return True
                else:
                    print(f'❌ LLVM translation failed: {translate_result.stderr[:200]}...')
                    return False
            return False
        except Exception as e:
            print(f'❌ Error creating lowered file: {e}')
            return False

    def process_file(self, input_file):
        """Complete pipeline to lower an MLIR file"""
        input_path = Path(input_file)
        if not input_path.exists():
            print(f'❌ Input file not found: {input_file}')
            return None
        print(f'🎯 Processing {input_file}')
        print(f'📊 Input size: {input_path.stat().st_size} bytes')
        available_passes = self.find_available_passes()
        successful_sequences = self.test_lowering_passes(str(input_path))
        if not successful_sequences:
            print('❌ No working lowering sequences found!')
            return None
        best_sequence = successful_sequences[0]
        print(f"\n🎯 Using best sequence: {' → '.join(best_sequence)}")
        output_file = str(input_path.parent / f'{input_path.stem}_lowered{input_path.suffix}')
        if self.create_lowered_file(str(input_path), output_file, best_sequence):
            print(f'🎉 Success! Lowered file created: {output_file}')
            return output_file
        else:
            print('❌ Failed to create lowered file')
            return None