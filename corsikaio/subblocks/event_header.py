import numpy as np


event_header_dtype_65 = np.dtype([
    ('event_header', 'S4'),  # 1
    ('event_number', 'float32'),  # 2
    ('particle_id', 'float32'),  # 3
    ('total_energy', 'float32'),  # 4
    ('starting_altitude', 'float32'),  # 5
    ('first_target_id', 'float32'),  # 6
    ('first_interaction_height', 'float32'),  # 7
    ('momentum_x', 'float32'),  # 8
    ('momentum_y', 'float32'),  # 9
    ('momentum_minus_z', 'float32'),  # 10
    ('zenith', 'float32'),  # 11
    ('azimuth', 'float32'),  # 12
    ('n_random_sequences', 'float32'),  # 13
    ('random_seeds', 'float32', (10, 3)),  # 14 - 43
    ('run_number', 'float32'),  # 44
    ('date', 'float32'),  # 45
    ('version', 'float32'),  # 46
    ('n_observation_levels', 'float32'),  # 47
    ('observation_height', 'float32', (10, )),  # 48 - 57
    ('energy_spectrum_slope', 'float32'),  # 58
    ('energy_min', 'float32'),  # 59
    ('energy_max', 'float32'),  # 60
    ('energy_cutoff_hadrons', 'float32'),  # 61
    ('energy_cutoff_muons', 'float32'),  # 62
    ('energy_cutoff_electrons', 'float32'),  # 63
    ('energy_cutoff_photons', 'float32'),  # 64
    ('nflain', 'float32'),  # 65
    ('nfdif', 'float32'),  # 66
    ('nflpi0', 'float32'),  # 67
    ('nflpif', 'float32'),  # 68
    ('nflche', 'float32'),  # 69
    ('nflfragm', 'float32'),  # 70
    ('earth_magnetic_field_x', 'float32'),  # 71
    ('earth_magnetic_field_z', 'float32'),  # 72
    ('egs4_flag', 'float32'),  # 73
    ('nkg_flag', 'float32'),  # 74
    ('low_energy_hadron_model', 'float32'),  # 75
    ('high_energy_hadron_model', 'float32'),  # 76
    ('cerenkov_flag', 'float32'),  # 77
    ('neutrino_flag', 'float32'),  # 78
    ('curved_flag', 'float32'),  # 79
    ('computer', 'float32'),  # 80
    ('theta_min', 'float32'),  # 81
    ('theta_max', 'float32'),  # 82
    ('phi_min', 'float32'),  # 83
    ('phi_max', 'float32'),  # 84
    ('cherenkov_bunch_size', 'float32'),  # 85
    ('n_cherenkov_detectors_x', 'float32'),  # 86
    ('n_cherenkov_detectors_y', 'float32'),  # 87
    ('cherenkov_detector_grid_spacing_x', 'float32'),  # 88
    ('cherenkov_detector_grid_spacing_y', 'float32'),  # 89
    ('cherenkov_detector_length_x', 'float32'),  # 90
    ('cherenkov_detector_length_y', 'float32'),  # 91
    ('cherenkov_output_flag', 'float32'),  # 92
    ('angle_array_x_magnetic_north', 'float32'),  # 93
    ('additional_muon_information_flag', 'float32'),  # 94
    ('egs4_multpliple_scattering_step_length_factor', 'float32'),  # 95
    ('cherenkov_wavelength_min', 'float32'),  # 96
    ('cherenkov_wavelength_max', 'float32'),  # 97
    ('n_reuse', 'float32'),  # 98
    ('reuse_x', 'float32', 20),  # 99 - 118
    ('reuse_y', 'float32', 20),  # 119 - 138
    ('sybill_interaction_flag', 'float32'),  # 139
    ('sybill_cross_section_flag', 'float32'),  # 140
    ('qgsjet_interaction_flag', 'float32'),  # 141
    ('qgsjet_cross_section_flag', 'float32'),  # 142
    ('dpmjet_interaction_flag', 'float32'),  # 143
    ('dpmjet_cross_section_flag', 'float32'),  # 144
    ('venus_nexus_epos_cross_section_flag', 'float32'),  # 145
    ('muon_multiple_scattering_flag', 'float32'),  # 146
    ('nkg_radial_distribution_range', 'float32'),  # 147
    ('energy_fraction_if_thinning_level_hadronic', 'float32'),  # 148
    ('energy_fraction_if_thinning_level_em', 'float32'),  # 149
    ('actual_weight_limit_thinning_hadronic', 'float32'),  # 150
    ('actual_weight_limit_thinning_em', 'float32'),  # 151
    ('max_radius_radial_thinning_cutting', 'float32'),  # 152
    ('viewcone_inner_angle', 'float32'),  # 153
    ('viewcone_outer_angle', 'float32'),  # 154
    ('transition_energy_low_high_energy_model', 'float32'),  # 155
    ('unused', 'float32', 118),
])


event_header_dtype_74 = np.dtype([
    ('event_header', 'S4'),  # 1
    ('event_number', 'float32'),  # 2
    ('particle_id', 'float32'),  # 3
    ('total_energy', 'float32'),  # 4
    ('starting_altitude', 'float32'),  # 5
    ('first_target_id', 'float32'),  # 6
    ('first_interaction_height', 'float32'),  # 7
    ('momentum_x', 'float32'),  # 8
    ('momentum_y', 'float32'),  # 9
    ('momentum_minus_z', 'float32'),  # 10
    ('zenith', 'float32'),  # 11
    ('azimuth', 'float32'),  # 12
    ('n_random_sequences', 'float32'),  # 13
    ('random_seeds', 'float32', (10, 3)),  # 14 - 43
    ('run_number', 'float32'),  # 44
    ('date', 'float32'),  # 45
    ('version', 'float32'),  # 46
    ('n_observation_levels', 'float32'),  # 47
    ('observation_height', 'float32', (10, )),  # 48 - 57
    ('energy_spectrum_slope', 'float32'),  # 58
    ('energy_min', 'float32'),  # 59
    ('energy_max', 'float32'),  # 60
    ('energy_cutoff_hadrons', 'float32'),  # 61
    ('energy_cutoff_muons', 'float32'),  # 62
    ('energy_cutoff_electrons', 'float32'),  # 63
    ('energy_cutoff_photons', 'float32'),  # 64
    ('nflain', 'float32'),  # 65
    ('nfdif', 'float32'),  # 66
    ('nflpi0', 'float32'),  # 67
    ('nflpif', 'float32'),  # 68
    ('nflche', 'float32'),  # 69
    ('nflfragm', 'float32'),  # 70
    ('earth_magnetic_field_x', 'float32'),  # 71
    ('earth_magnetic_field_z', 'float32'),  # 72
    ('egs4_flag', 'float32'),  # 73
    ('nkg_flag', 'float32'),  # 74
    ('low_energy_hadron_model', 'float32'),  # 75
    ('high_energy_hadron_model', 'float32'),  # 76
    ('cerenkov_flag', 'float32'),  # 77
    ('neutrino_flag', 'float32'),  # 78
    ('curved_flag', 'float32'),  # 79
    ('computer', 'float32'),  # 80
    ('theta_min', 'float32'),  # 81
    ('theta_max', 'float32'),  # 82
    ('phi_min', 'float32'),  # 83
    ('phi_max', 'float32'),  # 84
    ('cherenkov_bunch_size', 'float32'),  # 85
    ('n_cherenkov_detectors_x', 'float32'),  # 86
    ('n_cherenkov_detectors_y', 'float32'),  # 87
    ('cherenkov_detector_grid_spacing_x', 'float32'),  # 88
    ('cherenkov_detector_grid_spacing_y', 'float32'),  # 89
    ('cherenkov_detector_length_x', 'float32'),  # 90
    ('cherenkov_detector_length_y', 'float32'),  # 91
    ('cherenkov_output_flag', 'float32'),  # 92
    ('angle_array_x_magnetic_north', 'float32'),  # 93
    ('additional_muon_information_flag', 'float32'),  # 94
    ('egs4_multpliple_scattering_step_length_factor', 'float32'),  # 95
    ('cherenkov_wavelength_min', 'float32'),  # 96
    ('cherenkov_wavelength_max', 'float32'),  # 97
    ('n_reuse', 'float32'),  # 98
    ('reuse_x', 'float32', 20),  # 99 - 118
    ('reuse_y', 'float32', 20),  # 119 - 138
    ('sybill_interaction_flag', 'float32'),  # 139
    ('sybill_cross_section_flag', 'float32'),  # 140
    ('qgsjet_interaction_flag', 'float32'),  # 141
    ('qgsjet_cross_section_flag', 'float32'),  # 142
    ('dpmjet_interaction_flag', 'float32'),  # 143
    ('dpmjet_cross_section_flag', 'float32'),  # 144
    ('venus_nexus_epos_cross_section_flag', 'float32'),  # 145
    ('muon_multiple_scattering_flag', 'float32'),  # 146
    ('nkg_radial_distribution_range', 'float32'),  # 147
    ('energy_fraction_if_thinning_level_hadronic', 'float32'),  # 148
    ('energy_fraction_if_thinning_level_em', 'float32'),  # 149
    ('actual_weight_limit_thinning_hadronic', 'float32'),  # 150
    ('actual_weight_limit_thinning_em', 'float32'),  # 151
    ('max_radius_radial_thinning_cutting', 'float32'),  # 152
    ('viewcone_inner_angle', 'float32'),  # 153
    ('viewcone_outer_angle', 'float32'),  # 154
    ('transition_energy_low_high_energy_model', 'float32'),  # 155
    ('skimming_incidence_flag', 'float32'),  # 156
    ('horizontal_shower_exis_altitude', 'float32'),  # 157
    ('starting_height', 'float32'),  # 158
    ('explicit_charm_generation_flag', 'float32'),  # 159
    ('electromagnetic_subshower_hadronic_origin_output_flag', 'float32'),  # 160
    ('conex_min_vertical_depth', 'float32'),  # 161
    ('conex_high_energy_treshold_hadrons', 'float32'),  # 162
    ('conex_high_energy_treshold_muons', 'float32'),  # 163
    ('conex_high_energy_treshold_em', 'float32'),  # 164
    ('conex_low_energy_treshold_hadrons', 'float32'),  # 165
    ('conex_low_energy_treshold_muons', 'float32'),  # 166
    ('conex_low_energy_treshold_em', 'float32'),  # 167
    ('observaton_level_curvature_flag', 'float32'),  # 168
    ('conex_weight_limit_thinning_hadronic', 'float32'),  # 169
    ('conex_weight_limit_thinning_em', 'float32'),  # 170
    ('conex_weight_limit_sampling_hadronic', 'float32'),  # 171
    ('conex_weight_limit_sampling_muons', 'float32'),  # 172
    ('conex_weight_limit_sampling_em', 'float32'),  # 173
    ('unused', 'float32', 100),  # 174 - 273
])


event_header_dtype_75 = np.dtype([
    ('event_header', 'S4'),
    ('event_number', 'float32'),
    ('particle_id', 'float32'),
    ('total_energy', 'float32'),
    ('starting_altitude', 'float32'),
    ('first_target_id', 'float32'),
    ('first_interaction_height', 'float32'),
    ('momentum_x', 'float32'),
    ('momentum_y', 'float32'),
    ('momentum_minus_z', 'float32'),
    ('zenith', 'float32'),
    ('azimuth', 'float32'),
    ('n_random_sequences', 'float32'),
    ('random_seeds', 'float32', (10, 3)),
    ('run_number', 'float32'),
    ('date', 'float32'),
    ('version', 'float32'),
    ('n_observation_levels', 'float32'),
    ('observation_height', 'float32', (10, )),
    ('energy_spectrum_slope', 'float32'),
    ('energy_min', 'float32'),
    ('energy_max', 'float32'),
    ('energy_cutoff_hadrons', 'float32'),
    ('energy_cutoff_muons', 'float32'),
    ('energy_cutoff_electrons', 'float32'),
    ('energy_cutoff_photons', 'float32'),
    ('nflain', 'float32'),
    ('nfdif', 'float32'),
    ('nflpi0', 'float32'),
    ('nflpif', 'float32'),
    ('nflche', 'float32'),
    ('nflfragm', 'float32'),
    ('earth_magnetic_field_x', 'float32'),
    ('earth_magnetic_field_z', 'float32'),
    ('egs4_flag', 'float32'),
    ('nkg_flag', 'float32'),
    ('low_energy_hadron_model', 'float32'),
    ('high_energy_hadron_model', 'float32'),
    ('cerenkov_flag', 'float32'),
    ('neutrino_flag', 'float32'),
    ('curved_flag', 'float32'),
    ('computer', 'float32'),
    ('theta_min', 'float32'),
    ('theta_max', 'float32'),
    ('phi_min', 'float32'),
    ('phi_max', 'float32'),
    ('cherenkov_bunch_size', 'float32'),
    ('n_cherenkov_detectors_x', 'float32'),
    ('n_cherenkov_detectors_y', 'float32'),
    ('cherenkov_detector_grid_spacing_x', 'float32'),
    ('cherenkov_detector_grid_spacing_y', 'float32'),
    ('cherenkov_detector_length_x', 'float32'),
    ('cherenkov_detector_length_y', 'float32'),
    ('cherenkov_output_flag', 'float32'),
    ('angle_array_x_magnetic_north', 'float32'),
    ('additional_muon_information_flag', 'float32'),
    ('egs4_multpliple_scattering_step_length_factor', 'float32'),
    ('cherenkov_wavelength_min', 'float32'),
    ('cherenkov_wavelength_max', 'float32'),
    ('n_reuse', 'float32'),
    ('reuse_x', 'float32', 20),
    ('reuse_y', 'float32', 20),
    ('sybill_interaction_flag', 'float32'),
    ('sybill_cross_section_flag', 'float32'),
    ('qgsjet_interaction_flag', 'float32'),
    ('qgsjet_cross_section_flag', 'float32'),
    ('dpmjet_interaction_flag', 'float32'),
    ('dpmjet_cross_section_flag', 'float32'),
    ('venus_nexus_epos_cross_section_flag', 'float32'),
    ('muon_multiple_scattering_flag', 'float32'),
    ('nkg_radial_distribution_range', 'float32'),
    ('energy_fraction_if_thinning_level_hadronic', 'float32'),
    ('energy_fraction_if_thinning_level_em', 'float32'),
    ('actual_weight_limit_thinning_hadronic', 'float32'),
    ('actual_weight_limit_thinning_em', 'float32'),
    ('max_radius_radial_thinning_cutting', 'float32'),
    ('viewcone_inner_angle', 'float32'),
    ('viewcone_outer_angle', 'float32'),
    ('transition_energy_low_high_energy_model', 'float32'),
    ('skimming_incidence_flag', 'float32'),
    ('horizontal_shower_exis_altitude', 'float32'),
    ('starting_height', 'float32'),
    ('explicit_charm_generation_flag', 'float32'),
    ('electromagnetic_subshower_hadronic_origin_output_flag', 'float32'),
    ('conex_min_vertical_depth', 'float32'),
    ('conex_high_energy_treshold_hadrons', 'float32'),
    ('conex_high_energy_treshold_muons', 'float32'),
    ('conex_high_energy_treshold_em', 'float32'),
    ('conex_low_energy_treshold_hadrons', 'float32'),
    ('conex_low_energy_treshold_muons', 'float32'),
    ('conex_low_energy_treshold_em', 'float32'),
    ('observaton_level_curvature_flag', 'float32'),
    ('conex_weight_limit_thinning_hadronic', 'float32'),
    ('conex_weight_limit_thinning_em', 'float32'),
    ('conex_weight_limit_sampling_hadronic', 'float32'),
    ('conex_weight_limit_sampling_muons', 'float32'),
    ('conex_weight_limit_sampling_em', 'float32'),
    ('augerhit_stripes_half_width', 'float32'),
    ('augerhit_detector_distance', 'float32'),
    ('augerhit_reserved', 'float32'),
    ('n_multithin', 'float32'),
    ('multithin_energy_fraction_hadronic', 'float32', 6),
    ('multithin_weight_limit_hadronic', 'float32', 6),
    ('multithin_energy_fraction_em', 'float32', 6),
    ('multithin_weight_limit_em', 'float32', 6),
    ('multithin_random_seeds', 'float32', (6, 3)),
    ('icecube_energy_threshold', 'float32'),
    ('icecube_gzip_flag', 'float32'),
    ('icecube_pipe_flag', 'float32'),
    ('unused', 'float32', 51),
])
