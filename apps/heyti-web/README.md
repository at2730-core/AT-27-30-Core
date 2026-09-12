# HEYTI Web

Interfaz web de HEYTI-CORE V2.0.

## Estado

Fundación técnica inicial. La interfaz funcional, el Splash y la conexión con
HEYTI-CORE se incorporarán mediante cortes verticales certificados.

## Requisitos

- Node.js 24 LTS
- npm 11
- HEYTI-CORE disponible según el entorno configurado

## Comandos

```bash
npm install
npm run dev
npm run lint
npm run build
npm run preview

```

## Principios

- La interfaz no duplica reglas de negocio de CORE.
- Toda información muestra procedencia y estado de confianza.
- Los datos demostrativos deben identificarse explícitamente.
- El universo y el contexto territorial se comparten entre módulos.
- Las dependencias de producción se sirven localmente, sin CDN.

## Arquitectura

La aplicación vive en `apps/heyti-web` y consume HEYTI-CORE mediante contratos
versionados. No accede directamente a la base de datos ni a archivos fuente.
