import type {UniverseOption} from '../gateway/universe.client'
import type {UniverseSelection} from '../platform/platform.types'
import {scopeKey} from './contextQueries'
export function changeComparisonUniverse(current:UniverseSelection|null,choice:string,catalog:UniverseOption[],beforeChange:()=>void,select:(value:UniverseSelection)=>void):boolean {
 if(choice===scopeKey(current))return false
 const matches=catalog.filter(u=>`${u.level}:${u.id}`===choice)
 if(matches.length!==1)throw new Error('Selecciona un universo disponible en el catálogo.')
 const option=matches[0]
 if(!['state','municipality','federal-district','local-district'].includes(option.level)||!/^[1-9]\d*$/.test(option.id))throw new Error('Universo de comparación inválido.')
 const universe:UniverseSelection={id:option.id,level:option.level,label:option.label,parentId:option.level==='state'?null:'11',truthStatus:'pending'}
 beforeChange()
 select(universe)
 return true
}
