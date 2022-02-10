#  Copyright (c) 2021 Tobias Briones. All rights reserved.
#
#  SPDX-License-Identifier: BSD-3-Clause

"""
Contiene la implementación del modelo de muestreo virtual para suelo agrícola.
Author: Tobias Briones
"""

import random
import numpy as np
import pandas as pd
import geopandas as gpd
import plotly.express as px
from IPython.core.display import display

DEF_STRATUM_SAMPLING_SIZE = 0.8


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
        self.__n_threshold = 1

    def stratum_sampling_size(self, value):
        if value < 0 or value > 1:
            raise ValueError('Stratum Sampling Size is a floating percentage')
        self.__n = value

    def n_threshold(self, value):
        """
        Define un umbral para tomar en cuenta o no el valor de n para cada
        estrato. Es decir, si h_n <= value para el estrato h, entonces
        n = 1 y se tomará toda la población del estrato h para el MAS.
        """
        if value < 0:
            raise ValueError('N Threshold must be non-negative')
        self.__n_threshold = value

    def stratum_filter(self):
        return self.__stratum_filter

    def run(self):
        sampling = pd.DataFrame(self.__df, copy=True)

        sampling = self.__stratum_filter.filter_df(sampling)
        sampling = self.__stratified_random_sampling(sampling)
        sampling = sampling.reset_index(drop=True)
        return Result(
            sampling,
            self.__stratum_filter
        )

    def new_sampling_simulator(self):
        return SamplingSimulator(self.__n, self.__cols, self.__gis)

    def __stratified_random_sampling(self, df):
        grouped = df.groupby(self.__cols.stratum)
        sampled_strata = []

        for name, group in grouped:
            stratum_df = group.reset_index(drop=True)
            sample = self.__random_sampling(stratum_df)
            sampled_strata.append(sample)
        return pd.concat(sampled_strata)

    def __random_sampling(self, stratum_df):
        h_n = len(stratum_df)
        n = self.__n if h_n > self.__n_threshold else 1
        units = random.sample(range(0, h_n), int(n * h_n))
        return stratum_df.filter(items=units, axis=0)


class Result:
    """Define un muestreo virtual"""

    def __init__(
        self,
        sampling,
        stratum_filter
    ):
        self.__sampling = sampling
        self.__stratum_filter = stratum_filter

    def sampling(self):
        return self.__sampling

    def show_sampling(self):
        display(self.__sampling)

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

    def filter_df(self, df):
        self.filter()
        strata = self.to_list()
        significant_stratum = df[self.__cols.stratum].isin(strata)
        return df[significant_stratum]

    def filter(self):
        areas = self.stratum_areas()
        curated = areas[
            areas[self.__cols.harvested_area] > self.__area_threshold
            ]
        self.__result = curated.reset_index(drop=True)
        return self.__result

    def to_list(self):
        return list(self.__result[self.__cols.stratum])

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
