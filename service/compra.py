from db.conecction import conectar_bd
from model.compra import CompraPdf, CompraDetallePdf

def get_compra_id(idCompra: str) -> CompraPdf | None | str: 

    try:

        mydb = conectar_bd()
        mycursor = mydb.cursor()

        hora_formato = '%H:%i:%s'


        query = '''
                SELECT 
                DATE_FORMAT(c.fecha, '%d/%m/%Y') AS fecha, 
                DATE_FORMAT(c.hora, %s) AS hora,
                co.nombre AS comprobante,
                c.serie,
                c.numeracion,
                cn.documento,
                cn.informacion,
                cn.telefono,
                cn.celular,
                cn.email,
                cn.direccion,                
                al.nombre AS almacen,
                c.tipo,
                c.estado,
                c.observacion,
                c.nota,
                mo.codiso,
                mo.nombre AS moneda,
                CONCAT(us.nombres,' ',us.apellidos) AS usuario
            FROM 
                compra AS c
                INNER JOIN comprobante AS co ON co.idComprobante = c.idComprobante
                INNER JOIN moneda AS mo ON mo.idMoneda = c.idMoneda
                INNER JOIN almacen AS al ON al.idAlmacen = c.idAlmacen
                INNER JOIN clienteNatural AS cn ON cn.idCliente = c.idCliente
                INNER JOIN usuario AS us ON us.idUsuario = c.idUsuario 
            WHERE 
                c.idCompra = %s
            '''
        

        mycursor.execute(query, (hora_formato, idCompra))
        myresult = mycursor.fetchone()

        if myresult:  # Verifica si se encontró algún resultado

            row = myresult

            compra_pdf = CompraPdf(
                fecha=row[0],
                hora=row[1],
                comprobante=row[2],
                serie=row[3],
                numeracion=row[4],
                documento=row[5],
                informacion=row[6],
                telefono=row[7],
                celular=row[8],
                email=row[9],
                direccion=row[10],
                almacen=row[11],
                tipo=row[12],
                estado=row[13],
                observacion=row[14],
                nota=row[15],
                codiso=row[16],
                moneda=row[17],
                usuario=row[18] 
            )

            # column_names = [i[0] for i in mycursor.description]
            # row_dict = dict(zip(column_names, myresult))

            mydb.close()
            return compra_pdf  # Retorna el objeto
        else:
            mydb.close()
            return None 
    
    except Exception as err:
        mydb.close()  # Asegura cerrar la conexión en caso de error
        return f"Error de servidor: {err}" 
    

def get_compra_id_detalle(idCompra: str) -> list | str:
    
    try:

        mydb = conectar_bd()
        mycursor = mydb.cursor()

        query = '''
                SELECT 
                p.nombre AS producto,
                md.nombre AS medida, 
                m.nombre AS categoria, 
                cd.costo,
                cd.cantidad,
                cd.idImpuesto,
                imp.nombre AS impuesto,
                imp.porcentaje
            FROM compraDetalle AS cd 
                INNER JOIN producto AS p ON cd.idProducto = p.idProducto 
                INNER JOIN medida AS md ON md.idMedida = p.idMedida 
                INNER JOIN categoria AS m ON p.idCategoria = m.idCategoria 
                INNER JOIN impuesto AS imp ON cd.idImpuesto  = imp.idImpuesto  
            WHERE cd.idCompra = %s
        '''

        mycursor.execute(query,(idCompra,))
        myresult = mycursor.fetchall()

        result_list = []

        for row in myresult:
            detalle = CompraDetallePdf(
                producto=row[0],
                medida=row[1],
                categoria=row[2],
                costo=row[3],
                cantidad=row[4],
                idImpuesto=row[5],
                impuesto=row[6],
                porcentaje=row[7]
            )
            result_list.append(detalle)

        mydb.close()
        return result_list
    
    except Exception as err:
        mydb.close()  # Asegura cerrar la conexión en caso de error
        return f"Error de servidor: {err}" 