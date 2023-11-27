"""
Functions related to the CORSIKA longitudinal distribution
"""
import re
import numpy as np

PARTICLE_HEADER_RE = re.compile(r"LONGITUDINAL DISTRIBUTION IN\s+(\d+)\s+(SLANT|VERTICAL)\s+STEPS OF\s+(\d+(?:.\d*)?) G\/CM\*\*2 FOR SHOWER\s+(\d+)")
ENERGY_HEADER_RE = re.compile(r"LONGITUDINAL ENERGY DEPOSIT IN\s+(\d+)\s+(SLANT|VERTICAL)\s+STEPS OF\s+(\d+(?:.\d*)?) G\/CM\*\*2 FOR SHOWER\s+(\d+)")

ENERGY_COLUMNS = [
    "depth",
    "gamma", "em_ioniz", "em_cut", "mu_ioniz",
    "mu_cut", "hadr_ioniz", "hadr_cut", "neutrino", "sum"
]
PARTICLE_COLUMNS = [
    "depth",
    "gammas", "positrons", "electrons", "mu_plus", "mu_minus",
    "hadrons", "charged", "nuclei", "cherenkov"
]


def longitudinal_fit_function(depth, n_max, depth_0, depth_max, a, b, c):
    """
    The function CORSIKA fits to the longitudinal distribution.

    Parameters of this function are stored in the event end block
    in case the corresponding options of the LONGI keyword are set.

    Use like this:

    >>> depth = np.linspace(0, 1000, 100)
    >>> longitudinal_fit_function(depth, *event.end["longitudinal_fit_parameters"])
    """
    denominator =  (a + b * depth + c * depth**2)
    exponent = (depth_max - depth_0) / denominator
    power = ((depth - depth_0) / (depth_max - depth_0))**exponent
    exp = np.exp((depth_max - depth) / denominator)
    return n_max * power *  exp


def read_longitudinal_distributions(path):
    """
    Read longitudinal profiles from CORSIKA longitudinal file.

    This function returns a generator that iterates over air showers.

    Parameters
    ----------
    path : str, Path
        Path to CORSIKA longitudinal output file (DATXXXXXX.long)

    Yields
    ------
    longitudinal : dict
        Dict with the information for one air shower.
        Contains the longitudinal tables for "particles" and "energy_deposition"
        and the "parameters", "chi2_ndf" and "average_deviation" values of the 
        fit to the distribution if available.
    """
    first = True
    with open(path, "r") as f:
        try:
            line = f.readline().strip()
        except UnicodeDecodeError:
            raise IOError(f"Inputfile {path} does not seem to be a longitudinal file")

        while line:
            match = PARTICLE_HEADER_RE.match(line)
            if not match:
                if first:
                    raise IOError(f"Inputfile {path} does not seem to be a longitudinal file")
                else:
                    raise IOError(f"Error reading file, expected header line, got: {line}")
            first = False

            n_steps = int(match.group(1))
            longi = dict(
                shower=int(match.group(4)),
                n_steps=n_steps,
                slant=match.group(2) == "SLANT",
                step_width=float(match.group(3)),
            )

            # skip line with names
            f.readline()
            longi["particles"] = np.genfromtxt(
                f, max_rows=n_steps, names=PARTICLE_COLUMNS, dtype=None
            )

            line = f.readline().strip()
            match = ENERGY_HEADER_RE.match(line)
            if not match:
                raise IOError(f"Error reading file, expected energy deposition header line, got: {line}")
            n_steps = int(match.group(1))

            # skip
            f.readline()
            longi["energy_deposition"] = np.genfromtxt(f, max_rows=n_steps, names=ENERGY_COLUMNS, dtype=None)

            line = f.readline()
            if line.strip().startswith("FIT"):
                f.readline()
                parameters = f.readline().partition(" = ")[2]
                longi["parameters"] = np.array([float(p) for p in parameters.split()])

                chi2_ndf = f.readline().partition(" = ")[2]
                longi["chi2_ndf"] = float(chi2_ndf)

                deviation = f.readline().partition(" = ")[2]
                longi["average_deviation"] = float(deviation)

            f.readline()
            yield longi
            line = f.readline().strip()
