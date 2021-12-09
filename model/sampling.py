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

import numpy as np
import pandas as pd
import geopandas as gpd
import plotly.express as px
from IPython.core.display import display

DEF_STRATUM_SAMPLING_SIZE = 1_000


class Sampling:
    """
    Provee una implementación del muestreo aleatorio simple estratificado.
    """

    @staticmethod
    def from_main(main):
        return Sampling(main.gis(), main.df(), main.cols())

    def __init__(self, gis, df, cols):
        self.__gis = gis  # Immutable
        self.__df = df  # Immutable
        self.__cols = cols  # Immutable
        self.__n = DEF_STRATUM_SAMPLING_SIZE
        self.__stratum_filter = StratumFilter(df, cols)

    def stratum_sampling_size(self, value):
        self.__n = value

    def stratum_filter(self):
        return self.__stratum_filter

    def run(self):
        self.__stratum_filter.filter()
        return Result(
            self.__stratum_filter
        )

    def new_sampling_simulator(self):
        return SamplingSimulator(self.__n, self.__cols, self.__gis)


class Result:
    """Define un muestreo virtual"""

    def __init__(
        self,
        stratum_filter
    ):
        self.__stratum_filter = stratum_filter

    def show_stratum_filter(self):
        self.__stratum_filter.plot_stratum_areas()
        display(self.__stratum_filter.result())


class StratumFilter:
    def __init__(self, df, cols):
        self.__df = df
        self.__cols = cols
        self.__area_threshold = 0
        self.__result = pd.DataFrame()

    def area_threshold(self, value):
        self.__area_threshold = value

    def result(self):
        return self.__result

    def to_list(self):
        return list(self.__result[self.__cols.stratum])

    def filter(self):
        areas = self.stratum_areas()
        curated = areas[
            areas[self.__cols.harvested_area] > self.__area_threshold
            ]
        self.__result = curated.reset_index(drop=True)
        return self.__result

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


class SamplingSimulator:
    def __init__(self, h_n, cols, gis):  # Immutable
        self.__h_n = h_n
        self.__cols = cols
        self.__gis = gis

    def simulate(self, stratum):
        gdf = self.__gis.gdf()
        idx = self.__get_stratum_idx(stratum)

        for i, row in idx.iterrows():
            subset, subset_n = (row[self.__cols.gis_subset], int(row['n']))
            current_gdf = gdf[gdf[self.__cols.gis_subset] == subset]
            points = self.__random_points(subset_n, current_gdf)

            current_gdf.plot()
            points.plot()

    def __get_stratum_idx(self, stratum):
        """
        Calcula todos los subconjuntos del suelo agrícola que conforman
        el estrato dado y el tamaño de la muestra por subconjunto a
        tomar relativo al área de cada subconjunto.
        """

        df = self.__gis.df()
        sample_stratum = df[df[self.__cols.stratum] == stratum]
        total_area = sample_stratum[self.__cols.gis_area].squeeze().sum()
        sample_stratum.loc[:, 'weight'] = sample_stratum[
                                              self.__cols.gis_area
                                          ] / total_area
        sample_stratum.loc[:, 'n'] = sample_stratum['weight'] * self.__h_n

        return pd.DataFrame({
            self.__cols.gis_subset: sample_stratum[self.__cols.gis_subset],
            'n': sample_stratum['n']
        })

    @staticmethod
    def __random_points(n, gdf):
        """
        Calcula puntos aleatorios en los límites del mapa dado. Solo
        toma aquellos puntos válidos por lo que el total de puntos
        generados es menor o igual a n.
        """

        x_min, y_min, x_max, y_max = gdf.total_bounds
        x = np.random.uniform(x_min, x_max, n)
        y = np.random.uniform(y_min, y_max, n)

        points = gpd.GeoSeries(gpd.points_from_xy(x, y))
        points = points[points.within(gdf.unary_union)]
        return points
