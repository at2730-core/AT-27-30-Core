BEGIN;

INSERT INTO security.access_permission (
    permission_code,
    description,
    sensitive,
    audit_required
)
SELECT
    source.permission_code,
    source.description,
    FALSE,
    FALSE
FROM (
    VALUES
        (
            'SECTION_READ',
            'Consultar una seccion autorizada.'
        ),
        (
            'UNIVERSE_CATALOG_READ',
            'Consultar universos autorizados.'
        ),
        (
            'UNIVERSE_MAP_READ',
            'Consultar mapas de universos autorizados.'
        )
) AS source (
    permission_code,
    description
)
WHERE NOT EXISTS (
    SELECT 1
    FROM security.access_permission existing
    WHERE existing.permission_code = (
        source.permission_code
    )
);

UPDATE security.access_permission permission
SET
    description = source.description,
    sensitive = FALSE,
    audit_required = FALSE,
    active = TRUE
FROM (
    VALUES
        (
            'SECTION_READ',
            'Consultar una seccion autorizada.'
        ),
        (
            'UNIVERSE_CATALOG_READ',
            'Consultar universos autorizados.'
        ),
        (
            'UNIVERSE_MAP_READ',
            'Consultar mapas de universos autorizados.'
        )
) AS source (
    permission_code,
    description
)
WHERE permission.permission_code = (
    source.permission_code
);

INSERT INTO security.role_permission (
    role_id,
    permission_id,
    permission_scope
)
SELECT
    role.role_id,
    permission.permission_id,
    assignment.permission_scope
FROM (
    VALUES
        (
            'ADMINISTRATOR',
            'SECTION_READ',
            'GLOBAL'
        ),
        (
            'ADMINISTRATOR',
            'UNIVERSE_CATALOG_READ',
            'GLOBAL'
        ),
        (
            'ADMINISTRATOR',
            'UNIVERSE_MAP_READ',
            'GLOBAL'
        ),
        (
            'COORDINATOR',
            'SECTION_READ',
            'ASSIGNED_TERRITORY'
        ),
        (
            'COORDINATOR',
            'UNIVERSE_CATALOG_READ',
            'ASSIGNED_TERRITORY'
        ),
        (
            'COORDINATOR',
            'UNIVERSE_MAP_READ',
            'ASSIGNED_TERRITORY'
        )
) AS assignment (
    role_code,
    permission_code,
    permission_scope
)
JOIN security.access_role role
  ON role.role_code = assignment.role_code
JOIN security.access_permission permission
  ON permission.permission_code = (
        assignment.permission_code
     )
WHERE NOT EXISTS (
    SELECT 1
    FROM security.role_permission existing
    WHERE existing.role_id = role.role_id
      AND existing.permission_id = (
            permission.permission_id
          )
);

UPDATE security.role_permission existing
SET permission_scope = assignment.permission_scope
FROM (
    VALUES
        (
            'ADMINISTRATOR',
            'SECTION_READ',
            'GLOBAL'
        ),
        (
            'ADMINISTRATOR',
            'UNIVERSE_CATALOG_READ',
            'GLOBAL'
        ),
        (
            'ADMINISTRATOR',
            'UNIVERSE_MAP_READ',
            'GLOBAL'
        ),
        (
            'COORDINATOR',
            'SECTION_READ',
            'ASSIGNED_TERRITORY'
        ),
        (
            'COORDINATOR',
            'UNIVERSE_CATALOG_READ',
            'ASSIGNED_TERRITORY'
        ),
        (
            'COORDINATOR',
            'UNIVERSE_MAP_READ',
            'ASSIGNED_TERRITORY'
        )
) AS assignment (
    role_code,
    permission_code,
    permission_scope
)
JOIN security.access_role role
  ON role.role_code = assignment.role_code
JOIN security.access_permission permission
  ON permission.permission_code = (
        assignment.permission_code
     )
WHERE existing.role_id = role.role_id
  AND existing.permission_id = (
        permission.permission_id
      );

DO $validation$
DECLARE
    permission_count integer;
    assignment_count integer;
BEGIN
    SELECT COUNT(*)
    INTO permission_count
    FROM security.access_permission
    WHERE permission_code IN (
        'SECTION_READ',
        'UNIVERSE_CATALOG_READ',
        'UNIVERSE_MAP_READ'
    )
      AND active = TRUE;

    IF permission_count <> 3 THEN
        RAISE EXCEPTION
            'Conteo de permisos operativos invalido: %',
            permission_count;
    END IF;

    SELECT COUNT(*)
    INTO assignment_count
    FROM security.role_permission role_permission
    JOIN security.access_role role
      ON role.role_id = role_permission.role_id
    JOIN security.access_permission permission
      ON permission.permission_id = (
            role_permission.permission_id
         )
    WHERE (
            (
                role.role_code = 'ADMINISTRATOR'
                AND role_permission.permission_scope = 'GLOBAL'
            )
            OR (
                role.role_code = 'COORDINATOR'
                AND role_permission.permission_scope = (
                    'ASSIGNED_TERRITORY'
                )
            )
          )
      AND permission.permission_code IN (
            'SECTION_READ',
            'UNIVERSE_CATALOG_READ',
            'UNIVERSE_MAP_READ'
          );

    IF assignment_count <> 6 THEN
        RAISE EXCEPTION
            'Conteo de asignaciones operativas invalido: %',
            assignment_count;
    END IF;
END
$validation$;
COMMIT;
