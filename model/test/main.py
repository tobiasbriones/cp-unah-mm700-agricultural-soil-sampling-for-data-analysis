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

from . import hn_example as hn

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
    def new_instance(parent_dir='.'):
        gis = hn.Gis(parent_dir)
        df = hn.HardSampling.generate()
        return Main(gis, df)

    def __init__(self, gis, df):
        self.__gis = gis  # Immutable
        self.__df = df  # Immutable

    def gdf(self):
        return self.__gis.gdf

    def df(self):
        return self.__df

    def cols(self):
        return cols()

    def filter(self):
        valid_stratum = self.__df[DEF_STRATUM_COL] != hn.Stratum.NONE
        self.__df = self.__df[valid_stratum].reset_index(drop=True)


class ColumnConfig:
    """Define los atributos para el muestreo virtual"""

    def __init__(
        self,
        stratum='stratum',
        harvested_area='harvested_area',
        gis_area='area'
    ):
        self.stratum = stratum
        self.harvested_area = harvested_area
        self.gis_area = gis_area


def cols():
    return ColumnConfig(
        stratum=hn.STRATUM_COL,
        harvested_area=hn.HardSampling.HARVESTED_AREA_COL,
        gis_area=hn.Gis.AREA_COL
    )
