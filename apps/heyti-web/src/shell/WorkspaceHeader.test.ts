import { describe, expect, it } from 'vitest'

import type {
  TerritorialAccess,
} from '../gateway/auth.client'
import {
  territorialAccessLabel,
} from './WorkspaceHeader'


describe('etiqueta de alcance territorial', () => {
  it('describe la cobertura global', () => {
    const access: TerritorialAccess = {
      globalAccess: true,
      scopes: [
        {
          scopeId: 1,
          name: 'Acceso global',
          type: 'GLOBAL',
          municipality: null,
          sectionCount: 0,
        },
      ],
    }

    expect(
      territorialAccessLabel(access),
    ).toBe('Cobertura global')
  })

  it('describe el municipio asignado', () => {
    const access: TerritorialAccess = {
      globalAccess: false,
      scopes: [
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

    expect(
      territorialAccessLabel(access),
    ).toBe(
      'Municipio 20 ? Leon de los Aldama'
      + ' ? 787 secciones',
    )
  })

  it('identifica una sesion sin alcance', () => {
    expect(
      territorialAccessLabel({
        globalAccess: false,
        scopes: [],
      }),
    ).toBe('Sin alcance territorial')
  })

  it('resume alcances multiples', () => {
    const access: TerritorialAccess = {
      globalAccess: false,
      scopes: [
        {
          scopeId: 2,
          name: 'Leon',
          type: 'MUNICIPALITY',
          municipality: {
            municipalityId: 20,
            code: '20',
            name: 'Leon de los Aldama',
          },
          sectionCount: 787,
        },
        {
          scopeId: 3,
          name: 'Secciones adicionales',
          type: 'SECTION_SET',
          municipality: null,
          sectionCount: 2,
        },
      ],
    }

    expect(
      territorialAccessLabel(access),
    ).toBe('2 alcances territoriales')
  })
})
