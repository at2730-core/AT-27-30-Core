import {
  describe,
  expect,
  it,
} from 'vitest'
import type {
  TerritorialAccess,
} from '../gateway/auth.client'
import type {
  UniverseOption,
} from '../gateway/universe.client'
import {
  authenticatedDefaultUniverse,
} from './authenticatedUniverse'

const municipality: UniverseOption = {
  level: 'municipality',
  id: '20',
  label: 'Leon de los Aldama',
  sections: 787,
}

function access(
  globalAccess: boolean,
): TerritorialAccess {
  return {
    globalAccess,
    scopes: globalAccess
      ? [
          {
            scopeId: 3,
            name: 'Acceso global',
            type: 'GLOBAL',
            municipality: null,
            sectionCount: 0,
          },
        ]
      : [
          {
            scopeId: 2,
            name: 'Municipio 20 - Leon',
            type: 'MUNICIPALITY',
            municipality: {
              municipalityId: 20,
              code: '20',
              name: 'Leon de los Aldama',
            },
            sectionCount: 787,
          },
        ],
  }
}

describe(
  'universo predeterminado autenticado',
  () => {
    it(
      'selecciona el unico municipio autorizado',
      () => {
        expect(
          authenticatedDefaultUniverse(
            access(false),
            [municipality],
          ),
        ).toEqual({
          id: '20',
          label: 'Leon de los Aldama',
          level: 'municipality',
          parentId: '11',
          truthStatus: 'pending',
        })
      },
    )

    it(
      'no reemplaza el contexto del administrador',
      () => {
        expect(
          authenticatedDefaultUniverse(
            access(true),
            [municipality],
          ),
        ).toBeNull()
      },
    )

    it(
      'no inventa un universo sin catalogo',
      () => {
        expect(
          authenticatedDefaultUniverse(
            access(false),
            [],
          ),
        ).toBeNull()
      },
    )

    it(
      'no elige arbitrariamente entre varios universos',
      () => {
        expect(
          authenticatedDefaultUniverse(
            access(false),
            [
              municipality,
              {
                ...municipality,
                id: '1',
                label: 'Abasolo',
              },
            ],
          ),
        ).toBeNull()
      },
    )
  },
)
