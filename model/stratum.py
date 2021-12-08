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
Contiene modelos para los estratos del muestreo físico de cultivo de azúcares.

Author: Tobias Briones
"""

from strenum import StrEnum


class Stratum(StrEnum):
    """
    Define los estratos del muestreo físico. Contiene ejemplos comúnes de
    variedades de azúcares, lista que puede ser muy larga en un caso real e
    incluyendo variedades insignificantes que se deben demostrar como tales
    para realizar un filtrado por variedad.
    """

    NONE = 'Ninguno'
    CP_72_2086 = 'CP 72-2086'
    MEX_69_290 = 'Mex 69-290'
    MEX_79_431 = 'Mex 79-431'
    ITV_92_1424 = 'ITV 92-1424'
