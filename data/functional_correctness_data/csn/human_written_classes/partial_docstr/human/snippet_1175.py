import numpy as np

class SphericalRotator:
    """
    Base class for rotating points on a sphere.

    The input is a fiducial point (deg) which becomes (0, 0) in rotated coordinates.
    """

    def __init__(self, lon_ref, lat_ref, zenithal=False):
        self.setReference(lon_ref, lat_ref, zenithal)

    def setReference(self, lon_ref, lat_ref, zenithal=False):
        if zenithal:
            phi = np.pi / 2.0 + np.radians(lon_ref)
            theta = np.pi / 2.0 - np.radians(lat_ref)
            psi = 0.0
        if not zenithal:
            phi = -np.pi / 2.0 + np.radians(lon_ref)
            theta = np.radians(lat_ref)
            psi = np.radians(90.0)
        cos_psi, sin_psi = (np.cos(psi), np.sin(psi))
        cos_phi, sin_phi = (np.cos(phi), np.sin(phi))
        cos_theta, sin_theta = (np.cos(theta), np.sin(theta))
        self.rotation_matrix = np.array([[cos_psi * cos_phi - cos_theta * sin_phi * sin_psi, cos_psi * sin_phi + cos_theta * cos_phi * sin_psi, sin_psi * sin_theta], [-sin_psi * cos_phi - cos_theta * sin_phi * cos_psi, -sin_psi * sin_phi + cos_theta * cos_phi * cos_psi, cos_psi * sin_theta], [sin_theta * sin_phi, -sin_theta * cos_phi, cos_theta]])
        self.inverted_rotation_matrix = np.linalg.inv(self.rotation_matrix)

    def cartesian(self, lon, lat):
        lon = np.radians(lon)
        lat = np.radians(lat)
        x = np.cos(lat) * np.cos(lon)
        y = np.cos(lat) * np.sin(lon)
        z = np.sin(lat)
        return np.array([x, y, z])

    def rotate(self, lon, lat, invert=False):
        vec = self.cartesian(lon, lat)
        if invert:
            vec_prime = np.dot(np.array(self.inverted_rotation_matrix), vec)
        else:
            vec_prime = np.dot(np.array(self.rotation_matrix), vec)
        lon_prime = np.arctan2(vec_prime[1], vec_prime[0])
        lat_prime = np.arcsin(vec_prime[2])
        return (np.degrees(lon_prime) % 360.0, np.degrees(lat_prime))