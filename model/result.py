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
sampling.stratum_sampling_size(0.5)
sampling.n_threshold(100)

# Set up stratum filter
stratum_filter = sampling.stratum_filter()

stratum_filter.area_threshold(400)

# Run virtual sampling model
result = sampling.run()
sampled_df = result.sampling()

result.show_sampling()
result.show_stratum_filter()


# Test an application for the sample (yield analysis)

def get_yield(df):
    filtered_df = df[[hn.STRATUM_COL, hn.HardSampling.YIELD_COL,
                      hn.HardSampling.HARVESTED_AREA_COL]]
    product_df = filtered_df.copy(deep=True)
    product_df['Product'] = product_df[hn.HardSampling.YIELD_COL] * product_df[
        hn.HardSampling.HARVESTED_AREA_COL]
    dot = product_df.groupby(hn.STRATUM_COL).sum()
    dot['Rendimiento'] = dot['Product'] / dot[
        hn.HardSampling.HARVESTED_AREA_COL]
    return dot.reset_index().drop('Product', axis=1)


# The sampled yield computation should be pretty similar to the original one
sampled_yield = get_yield(sampled_df)
real_yield = get_yield(hard_sampling)

merge_df = real_yield[[hn.STRATUM_COL, 'Rendimiento']]
merge_df = merge_df.rename(columns={'Rendimiento': 'Rendimiento Real'})

sampled_yield = sampled_yield.merge(merge_df, on=hn.STRATUM_COL, how='left')

sampled_yield['Error relativo (%)'] = (abs(
    sampled_yield['Rendimiento'] - sampled_yield['Rendimiento Real']) /
                                       sampled_yield['Rendimiento Real']) * 100

# display(real_yield)
display(sampled_yield)
