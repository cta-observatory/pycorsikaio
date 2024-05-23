import warnings
from collections import defaultdict

from .dtypes import Field, build_dtype

event_header_fields_65 = [
    Field(1, "event_header", dtype="S4"),
    Field(2, "event_number"),
    Field(3, "particle_id"),
    Field(4, "total_energy", unit="GeV"),
    Field(5, "starting_altitude", unit="g/cm2"),
    Field(6, "first_target_id"),
    Field(7, "first_interaction_height", unit="cm"),
    Field(8, "momentum_x", unit="GeV/c"),
    Field(9, "momentum_y", unit="GeV/c"),
    Field(10, "momentum_minus_z", unit="GeV/c"),
    Field(11, "zenith", unit="rad"),
    Field(12, "azimuth", unit="rad"),
    Field(13, "n_random_sequences"),
    Field(13 + 1, "random_seeds", shape=(10, 3)),
    Field(44, "run_number"),
    Field(45, "date"),
    Field(46, "version"),
    Field(47, "n_observation_levels"),
    Field(47 + 1, "observation_height", unit="cm", shape=10),
    Field(58, "energy_spectrum_slope"),
    Field(59, "energy_min", unit="GeV"),
    Field(60, "energy_max", unit="GeV"),
    Field(61, "energy_cutoff_hadrons", unit="GeV"),
    Field(62, "energy_cutoff_muons", unit="GeV"),
    Field(63, "energy_cutoff_electrons", unit="GeV"),
    Field(64, "energy_cutoff_photons", unit="GeV"),
    Field(65, "nflain"),
    Field(66, "nfdif"),
    Field(67, "nflpi0"),
    Field(68, "nflpif"),
    Field(69, "nflche"),
    Field(70, "nfragm"),
    Field(71, "earth_magnetic_field_x", unit="uT"),
    Field(72, "earth_magnetic_field_z", unit="uT"),
    Field(73, "egs4_flag"),
    Field(74, "nkg_flag"),
    Field(75, "low_energy_hadron_model"),
    Field(76, "high_energy_hadron_model"),
    Field(77, "cerenkov_flag"),
    Field(78, "neutrino_flag"),
    Field(79, "curved_flag"),
    Field(80, "computer"),
    Field(81, "theta_min", unit="deg"),
    Field(82, "theta_max", unit="deg"),
    Field(83, "phi_min", unit="deg"),
    Field(84, "phi_max", unit="deg"),
    Field(85, "cherenkov_bunch_size"),
    Field(86, "n_cherenkov_detectors_x"),
    Field(87, "n_cherenkov_detectors_y"),
    Field(88, "cherenkov_detector_grid_spacing_x", unit="cm"),
    Field(89, "cherenkov_detector_grid_spacing_y", unit="cm"),
    Field(90, "cherenkov_detector_length_x", unit="cm"),
    Field(91, "cherenkov_detector_length_y", unit="cm"),
    Field(92, "cherenkov_output_flag"),
    Field(93, "angle_array_x_magnetic_north", unit="rad"),
    Field(94, "additional_muon_information_flag"),
    Field(95, "egs4_multpliple_scattering_step_length_factor"),
    Field(96, "cherenkov_wavelength_min", unit="nm"),
    Field(97, "cherenkov_wavelength_max", unit="nm"),
    Field(98, "n_reuse"),
    Field(98 + 1, "reuse_x", shape=20),
    Field(118 + 1, "reuse_y", shape=20),
    Field(139, "sybill_interaction_flag"),
    Field(140, "sybill_cross_section_flag"),
    Field(141, "qgsjet_interaction_flag"),
    Field(142, "qgsjet_cross_section_flag"),
    Field(143, "dpmjet_interaction_flag"),
    Field(144, "dpmjet_cross_section_flag"),
    Field(145, "venus_nexus_epos_cross_section_flag"),
    Field(146, "muon_multiple_scattering_flag"),
    Field(147, "nkg_radial_distribution_range", unit="cm"),
    Field(148, "energy_fraction_if_thinning_level_hadronic"),
    Field(149, "energy_fraction_if_thinning_level_em"),
    Field(150, "actual_weight_limit_thinning_hadronic"),
    Field(151, "actual_weight_limit_thinning_em"),
    Field(152, "max_radius_radial_thinning_cutting", unit="cm"),
    Field(153, "viewcone_inner_angle", unit="deg"),
    Field(154, "viewcone_outer_angle", unit="deg"),
    Field(155, "transition_energy_low_high_energy_model", unit="GeV"),
]


event_header_fields_73 = event_header_fields_65 + [
    Field(156, "skimming_incidence_flag"),
    Field(157, "horizontal_shower_exis_altitude", unit="cm"),
    Field(158, "starting_height", unit="cm"),
    Field(159, "explicit_charm_generation_flag"),
    Field(160, "electromagnetic_subshower_hadronic_origin_output_flag"),
    Field(161, "conex_min_vertical_depth", unit="g/cm2"),
    Field(162, "conex_high_energy_treshold_hadrons", unit="GeV"),
    Field(163, "conex_high_energy_treshold_muons", unit="GeV"),
    Field(164, "conex_high_energy_treshold_em", unit="GeV"),
    Field(165, "conex_low_energy_treshold_hadrons", unit="GeV"),
    Field(166, "conex_low_energy_treshold_muons", unit="GeV"),
    Field(167, "conex_low_energy_treshold_em", unit="GeV"),
    Field(168, "observaton_level_curvature_flag"),
    Field(169, "conex_weight_limit_thinning_hadronic"),
    Field(170, "conex_weight_limit_thinning_em"),
    Field(171, "conex_weight_limit_sampling_hadronic"),
    Field(172, "conex_weight_limit_sampling_muons"),
    Field(173, "conex_weight_limit_sampling_em"),
]

event_header_fields_74 = event_header_fields_73.copy()

event_header_fields_75 = event_header_fields_74 + [
    Field(174, "augerhit_stripes_half_width", unit="cm"),
    Field(175, "augerhit_detector_distance", unit="cm"),
    Field(176, "augerhit_reserved"),
    Field(177, "n_multithin"),
    Field(177 + 1, "multithin_energy_fraction_hadronic", shape=6),
    Field(183 + 1, "multithin_weight_limit_hadronic", shape=6),
    Field(189 + 1, "multithin_energy_fraction_em", shape=6),
    Field(195 + 1, "multithin_weight_limit_em", shape=6),
    Field(199 + 3, "multithin_random_seeds", shape=(6, 3)),
    Field(220, "icecube_energy_threshold", unit="GeV"),
    Field(221, "icecube_gzip_flag"),
    Field(222, "icecube_pipe_flag"),
]
event_header_fields_76 = event_header_fields_75.copy()
event_header_fields_77 = event_header_fields_76.copy()

event_header_dtype_65xxx = build_dtype(event_header_fields_65)
event_header_dtype_73xxx = build_dtype(event_header_fields_73)
event_header_dtype_74xxx = build_dtype(event_header_fields_74)
event_header_dtype_75xxx = build_dtype(event_header_fields_75)
event_header_dtype_76xxx = build_dtype(event_header_fields_76)
event_header_dtype_77xxx = build_dtype(event_header_fields_77)

event_header_thin_dtype_65xxx = build_dtype(event_header_fields_65, itemsize = 4 * 312)
event_header_thin_dtype_73xxx = build_dtype(event_header_fields_73, itemsize = 4 * 312)
event_header_thin_dtype_74xxx = build_dtype(event_header_fields_74, itemsize = 4 * 312)
event_header_thin_dtype_75xxx = build_dtype(event_header_fields_75, itemsize = 4 * 312)
event_header_thin_dtype_76xxx = build_dtype(event_header_fields_76, itemsize = 4 * 312)
event_header_thin_dtype_77xxx = build_dtype(event_header_fields_77, itemsize = 4 * 312)

def warn_dtype():
    warnings.warn("Version unknown, using event header dtype definition of version 7.7XXX")
    return event_header_dtype_77xxx

def warn_dtype_thin():
    warnings.warn("Version unknown, using event header definition dtype of version 7.7XXX")
    return event_header_thin_dtype_77xxx

def warn_fields():
    warnings.warn("Version unknown, using event header fields definition of version 7.7XXX")
    return event_header_fields_77

event_header_fields = defaultdict(warn_fields)
event_header_fields[6.5] = event_header_fields_65
event_header_fields[7.3] = event_header_fields_73
event_header_fields[7.4] = event_header_fields_74
event_header_fields[7.5] = event_header_fields_75
event_header_fields[7.6] = event_header_fields_76
event_header_fields[7.7] = event_header_fields_77

event_header_types = defaultdict(warn_dtype)
event_header_types[6.5] = event_header_dtype_65xxx
event_header_types[7.3] = event_header_dtype_73xxx
event_header_types[7.4] = event_header_dtype_74xxx
event_header_types[7.5] = event_header_dtype_75xxx
event_header_types[7.6] = event_header_dtype_76xxx
event_header_types[7.7] = event_header_dtype_76xxx

event_header_thin_types = defaultdict(warn_dtype_thin)
event_header_thin_types[6.5] = event_header_thin_dtype_65xxx
event_header_thin_types[7.3] = event_header_thin_dtype_73xxx
event_header_thin_types[7.4] = event_header_thin_dtype_74xxx
event_header_thin_types[7.5] = event_header_thin_dtype_75xxx
event_header_thin_types[7.6] = event_header_thin_dtype_76xxx
event_header_thin_types[7.7] = event_header_thin_dtype_76xxx
