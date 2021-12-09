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

import random
import functools
import numpy as np
import pandas as pd
import geopandas as gpd
from strenum import StrEnum

# Definición de los datos geográficos

GIS_FILE_NAME = '/data/gis/gadm36_HND_1.shp'
DEPARTMENT_COL = 'NAME_1'
STRATUM_COL = 'Estrato'
AREA_COL = 'Área Departamento (HA)'


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


def get_hn_df():
    departments = [
        'Atlántida',
        'Choluteca',
        'Colón',
        'Comayagua',
        'Copán',
        'Cortés',
        'El Paraíso',
        'Francisco Morazán',
        'Gracias a Dios',
        'Intibucá',
        'Islas de la Bahía',
        'La Paz',
        'Lempira',
        'Ocotepeque',
        'Olancho',
        'Santa Bárbara',
        'Valle',
        'Yoro'
    ]

    strata = [
        Stratum.CP_72_2086,
        Stratum.NONE,
        Stratum.MEX_79_431,
        Stratum.ITV_92_1424,
        Stratum.MEX_79_431,
        Stratum.CP_72_2086,
        Stratum.CP_72_2086,
        Stratum.MEX_69_290,
        Stratum.ITV_92_1424,
        Stratum.NONE,
        Stratum.NONE,
        Stratum.MEX_69_290,
        Stratum.CP_72_2086,
        Stratum.CP_72_2086,
        Stratum.MEX_69_290,
        Stratum.MEX_79_431,
        Stratum.NONE,
        Stratum.CP_72_2086
    ]

    areas_km2 = [
        4227,
        4397,
        8875,
        5120,
        3239,
        3911,
        7383,
        8619,
        15876,
        3126,
        229,
        2534,
        4285,
        1636,
        24038,
        5013,
        1618,
        7787
    ]  # https://es.wikipedia.org/wiki/Organizaci%C3%B3n_territorial_de_Honduras

    areas_ha = list(map(lambda a: a * 100, areas_km2))

    return pd.DataFrame({
        DEPARTMENT_COL: departments,
        STRATUM_COL: strata,
        AREA_COL: areas_ha
    })


def get_hn_gdf(hn_df, rel_parent='.'):
    gdf_data = gpd.read_file(rel_parent + GIS_FILE_NAME)
    return gpd.GeoDataFrame(hn_df, geometry=gdf_data.geometry)


# Definición de los datos del muestreo físico

YIELD_COL = 'TA/HA Real'  # Toneladas de Azúcar por Hectárea (Rendimiento)
HARVESTED_AREA_COL = 'Área Cosechada (HA)'
POPULATION_SIZE = 100_000


def generate_psampling():
    """
    Genera el conjunto de datos correspondientes a un año a partir de
    valores aleatorios con cierto criterio de acuerdo al problema planteado.
    """
    variety_data = pd.DataFrame(
        random.choices(list(Stratum), k=POPULATION_SIZE), columns=[STRATUM_COL]
    )
    area_data = pd.DataFrame(
        np.random.randint(0.1, 50_000, (POPULATION_SIZE, 1)) / 10,
        columns=[HARVESTED_AREA_COL]
    )
    yield_data = pd.DataFrame(
        np.random.randint(0, 100, (POPULATION_SIZE, 1)) / 10,
        columns=[YIELD_COL]
    )
    data = [variety_data, area_data, yield_data]
    return functools.reduce(
        lambda left, right: pd.merge(
            left,
            right,
            left_index=True,
            right_index=True
        ),
        data
    )
