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

DEF_STRATUM_SAMPLING_SIZE = 1_000


class Sampling:
    """
    Provee una implementación del muestreo aleatorio simple estratificado.
    """

    @staticmethod
    def from_main(main):
        return Sampling(main.gdf(), main.df())

    def __init__(self, gdf, df):
        self.__gdf = gdf  # Immutable
        self.__df = df  # Immutable
        self.__n = DEF_STRATUM_SAMPLING_SIZE
        self.__stratum_col = 'Stratum'

    def stratum_sampling_size(self, n):
        self.__n = n

    def stratum_col(self, col):
        self.__stratum_col = col

    def run(self):
        return Result()


class Result:
    """Define un muestreo virtual"""

    def __init__(self):
        pass
