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
Contiene modelos para el conjunto de datos de entrada consistente en los datos
geográficos y los datos del muestreo físico.

Author: Tobias Briones
"""

import pandas as pd
import geopandas as gpd
from model.stratum import Stratum

DEF_STRATUM_COL = 'Estrato'


class Main:
    """
    Define la estructura y comportamiento del conjunto de datos geográfico y de
    muestreo físico del suelo agrícola. Analiza un archivo shapefile (.shp)
    conteniendo el mapa del área agrícola particionada por estratos (
    probablemente variedad de cultivo) y un DataFrame conteniendo los datos
    del muestreo físico. La variable independiente del conjunto de datos está
    dada por estrato.
    """

    @staticmethod
    def from_shp(path, df):
        gdf_data = gpd.read_file(path)
        gdf = gpd.GeoDataFrame(df, geometry=gdf_data.geometry)
        return Main(gdf)

    def __init__(self, gdf):
        self.__gdf = gdf  # Immutable
        self.__df = self.__get_df()

    def gdf(self):
        return self.__gdf

    def df(self):
        return self.__df

    def filter(self):
        filter = self.__df[DEF_STRATUM_COL] != Stratum.NONE
        self.__df = self.__df[filter].reset_index(drop=True)
        #
        # Aquí va el filtro por umbral de área cosechada
        #

    def __get_df(self):
        gdf = self.__gdf.drop(columns='geometry')
        return pd.DataFrame(gdf, copy=True)
