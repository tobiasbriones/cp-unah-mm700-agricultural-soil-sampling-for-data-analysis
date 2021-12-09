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

import matplotlib.pyplot as plt


def plot(gdf, title, size=10):
    fig, ax = plt.subplots(1)

    gdf.plot(ax=ax)
    ax.set_title(title)
    fig.set_figwidth(size)
    fig.set_figheight(size)
    plt.show()
