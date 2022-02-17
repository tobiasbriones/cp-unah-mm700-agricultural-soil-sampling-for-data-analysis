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
