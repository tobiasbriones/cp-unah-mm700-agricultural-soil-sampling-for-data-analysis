#  Copyright (c) 2021 Tobias Briones. All rights reserved.
#
#  SPDX-License-Identifier: BSD-3-Clause
#
#  This file is part of Course Project at UNAH-MM700: Agricultural Soil Sampling
#  for Data Analysis.
#
#  This source code is licensed under the BSD-3-Clause License found in the
#  LICENSE-BSD file in the root directory of this source tree or at
#  https://opensource.org/licenses/BSD-3-Clause.

import sampling
from test import main

# Check the notebook for more insight

main = main.Main.new_instance('./test')
sampling = sampling.Sampling.from_main(main)

# Print dataframe
# main.df()

# Set up sampling
sampling.stratum_sampling_size(400)

# Set up stratum filter
stratum_filter = sampling.stratum_filter()
stratum_filter.area_threshold(2_480_000)

# Run virtual sampling model
result = sampling.run()
sampled_df = result.sampling()

result.show_sampling()
result.show_stratum_filter()

# Yield output
# Test the results

def get_yield(df):
    grouped = df.groupby(hn.STRATUM_COL)
    abs_yield = grouped[hn.HardSampling.YIELD_COL].sum().reset_index()
    abs_areas = grouped[hn.HardSampling.HARVESTED_AREA_COL].sum().reset_index()
    yield_result = abs_yield.merge(abs_areas)
    yield_result["Rendimiento"] = abs_yield[hn.HardSampling.YIELD_COL] / abs_areas[hn.HardSampling.HARVESTED_AREA_COL]
    return yield_result

# The sampled yield computation should be pretty similar to the original one

sampled_yield = get_yield(sampled_df)
real_yield = get_yield(hard_sampling)

sampled_yield['Rendimiento real'] = real_yield['Rendimiento']
sampled_yield['Error relativo (%)'] = (abs(sampled_yield['Rendimiento'] - real_yield['Rendimiento']) / real_yield['Rendimiento']) * 100
