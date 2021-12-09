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

"""
Contiene la implementación del modelo de muestreo virtual para suelo agrícola.

Author: Tobias Briones
"""
import pandas as pd
import plotly.express as px

DEF_STRATUM_SAMPLING_SIZE = 1_000


class Sampling:
    """
    Provee una implementación del muestreo aleatorio simple estratificado.
    """

    @staticmethod
    def from_main(main):
        return Sampling(main.gdf(), main.df(), main.cols())

    def __init__(self, gdf, df, cols):
        self.__gdf = gdf  # Immutable
        self.__df = df  # Immutable
        self.__cols = cols  # Immutable
        self.__n = DEF_STRATUM_SAMPLING_SIZE
        self.__stratum_filter = StratumFilter(df, cols)

    def stratum_sampling_size(self, value):
        self.__n = value

    def stratum_filter(self):
        return self.__stratum_filter

    def run(self):
        result = Result()

        strata = self.__stratum_filter.filter()
        return result


class Result:
    """Define un muestreo virtual"""

    def __init__(
        self,
        strata=pd.DataFrame()
    ):
        self.strata = strata


class StratumFilter:
    def __init__(self, df, cols):
        self.__df = df
        self.__cols = cols
        self.__area_threshold = 0

    def area_threshold(self, value):
        self.__area_threshold = value

    def filter(self):
        areas = self.stratum_areas()
        curated = areas[
            areas[self.__cols.harvested_area] > self.__area_threshold
            ]
        return curated.reset_index(drop=True)

    def plot_stratum_areas(self):
        fig = px.bar(
            self.stratum_areas(),
            x=self.__cols.stratum,
            y=self.__cols.harvested_area
        )

        fig.show()

    def stratum_areas(self):
        grouped = self.__df.groupby(self.__cols.stratum)[
            self.__cols.harvested_area
        ]
        return grouped.sum().reset_index()
