from sqlalchemy import text
from db.connection import Session

def obtener_transacciones(fecha_inicio: str, fecha_final: str, id_sucursal: str, id_usuario: str):
    try:
        db = Session(expire_on_commit=False)

        query = text('''
        SELECT 
            -- 
            CASE 
                WHEN c.idVenta IS NOT NULL THEN co.nombre
                ELSE 'COBRO'
            END AS concepto,
            --
            COUNT(*) AS cantidad,
            -- 
            CASE 
                WHEN c.idVenta IS NOT NULL THEN moc.codiso
                ELSE  mog.codiso
            END AS codiso,
            SUM(i.monto) AS ingreso,
            0 AS salida
        FROM ingreso AS i
        -- 
        LEFT JOIN venta AS c ON c.idVenta = i.idVenta
        LEFT JOIN concepto AS co ON co.idConcepto = c.idConcepto
        LEFT JOIN moneda AS moc ON moc.idMoneda = c.idMoneda
        -- 
        LEFT JOIN cobro AS g ON g.idCobro = i.idCobro
        LEFT JOIN moneda AS mog ON mog.idMoneda = g.idMoneda
        WHERE 
        (c.fecha BETWEEN :fecha_inicio AND :fecha_final OR g.fecha BETWEEN :fecha_inicio AND :fecha_final) AND (
            (:id_sucursal = '' AND :id_usuario = '') 
            OR
            (:id_sucursal <> '' AND (c.idSucursal = :id_sucursal OR g.idSucursal = :id_sucursal) AND :id_usuario = '') 
            OR
            (:id_sucursal = '' AND :id_usuario <> '' AND (c.idUsuario = :id_usuario OR g.idUsuario = :id_usuario))
            OR
            (:id_sucursal <> '' AND (c.idSucursal = :id_sucursal OR g.idSucursal = :id_sucursal) AND :id_usuario <> '' AND (c.idUsuario = :id_usuario OR g.idUsuario = :id_usuario))
        )
        GROUP BY 
            concepto
        --
        UNION
        --
        SELECT 
            --
            CASE 
                WHEN c.idCompra IS NOT NULL THEN co.nombre
                ELSE 'GASTO'
            END AS concepto,
            --
            COUNT(*) AS cantidad,
            --
            CASE 
                WHEN c.idCompra IS NOT NULL THEN moc.codiso
                ELSE  mog.codiso
            END AS codiso,
            0 as ingreso,
            SUM(-s.monto) AS salida
        FROM salida AS s
        LEFT JOIN compra AS c ON c.idCompra = s.idCompra
        LEFT JOIN concepto AS co ON co.idConcepto = c.idConcepto
        LEFT JOIN moneda AS moc ON moc.idMoneda = c.idMoneda
        --
        LEFT JOIN gasto AS g ON g.idGasto = s.idGasto
        LEFT JOIN moneda AS mog ON mog.idMoneda = g.idMoneda
        WHERE 
        (c.fecha BETWEEN :fecha_inicio AND :fecha_final OR g.fecha BETWEEN :fecha_inicio AND :fecha_final) AND (
            (:id_sucursal = '' AND :id_usuario = '') 
            OR
            (:id_sucursal <> '' AND (c.idSucursal = :id_sucursal OR g.idSucursal = :id_sucursal) AND :id_usuario = '') 
            OR
            (:id_sucursal = '' AND :id_usuario <> '' AND (c.idUsuario = :id_usuario OR g.idUsuario = :id_usuario))
            OR
            (:id_sucursal <> '' AND (c.idSucursal = :id_sucursal OR g.idSucursal = :id_sucursal) AND :id_usuario <> '' AND (c.idUsuario = :id_usuario OR g.idUsuario = :id_usuario))
        )
        GROUP BY 
            concepto
        ''').bindparams(fecha_inicio=fecha_inicio,
                        fecha_final=fecha_final,
                        id_sucursal=id_sucursal,
                        id_usuario=id_usuario)
        
        resultado = db.execute(query).all()

        return resultado
    finally:
        db.close()


def obtener_bancos(fecha_inicio: str, fecha_final: str, id_sucursal: str, id_usuario: str):
    try:
        db = Session(expire_on_commit=False)

        query = text('''
        SELECT 
            b.nombre,
            SUM(CASE 
                WHEN bd.tipo = 1 THEN bd.monto  
                ELSE -bd.monto
            END) AS monto
        FROM 
            banco as b 
        INNER JOIN 
            bancoDetalle as bd on b.idBanco = bd.idBanco
        WHERE
        bd.fecha BETWEEN :fecha_inicio AND :fecha_final AND (
            (:id_sucursal = '' AND :id_usuario = '')
            OR
            (:id_sucursal <> '' AND b.idSucursal = :id_sucursal AND :id_usuario = '')
            OR
            (:id_sucursal = '' AND :id_usuario <> '' AND bd.idUsuario =:id_usuario)
            OR
            (:id_sucursal <> '' AND b.idSucursal = :id_sucursal AND :id_usuario <> '' AND bd.idUsuario = :id_usuario)
        )
        GROUP BY 
            b.idBanco
        ''').bindparams(fecha_inicio=fecha_inicio,
                        fecha_final=fecha_final,
                        id_sucursal=id_sucursal,
                        id_usuario=id_usuario)

        resultado = db.execute(query).all()

        return resultado
    finally:
        db.close()
