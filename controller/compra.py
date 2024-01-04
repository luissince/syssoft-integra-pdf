from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse

# from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse
from jinja2 import Environment, FileSystemLoader

from service.compra import get_compra_id, get_compra_id_detalle
from model.response import response_Custom_Error
from pdf.pdf_compra import generar_ticket, generar_a4
from helper.tools import impuestos_generados_compra, calculate_tax_bruto, calculate_tax

from decimal import Decimal, ROUND_HALF_UP

routerCompra = APIRouter()

tagCompra = "Compra"


@routerCompra.get('/ticket/{id_compra}', tags=[tagCompra])
async def generar_pdf_ticket(id_compra: str):
    try:

        # id_compra = 'CP0001'

        obj = get_compra_id(id_compra)

        if obj is None:
            resp = response_Custom_Error("No se encontron resultados")
            return JSONResponse(resp, status_code=500)

        if isinstance(obj, str):
            resp = response_Custom_Error(str(obj))
            return JSONResponse(resp, status_code=500)
        
        compra = obj.__dict__


        obj_det = get_compra_id_detalle(id_compra)

        if isinstance(obj_det, str):
            resp = response_Custom_Error(str(obj_det))
            return JSONResponse(resp, status_code=500)
        

        impuestos = impuestos_generados_compra(obj_det)
        primer_impuesto = impuestos[0]
        
        sub_total = 0
        total = 0

        for item in obj_det:
            cantidad = item.cantidad
            valor = item.costo
            impuesto = item.porcentaje

            valor_actual = cantidad * valor
            valor_sub_neto = calculate_tax_bruto(impuesto, valor_actual)
            valor_impuesto = calculate_tax(impuesto, valor_sub_neto)
            valor_neto = valor_sub_neto + valor_impuesto

            sub_total += valor_sub_neto
            total += valor_neto

        data_html = {

            "title": "PDF compra",

            # Datos empresa
            "empresa": "INVERSIONES KALLPAY DEL SUR S.A.C.",
            "ruc": "20102020511",
            "direccion_emp": "Av. Benavides 4040",
            "ubigeo_emp": "Junin Huancayo Huancayo",
            "telefono": "956672465",
            "email": "silvabasauri@gmail.com",

            #Datos comprobante
            "comprobante": compra["comprobante"],
            "serie": compra["serie"],
            "numeracion": compra["numeracion"],
            "fecha": compra["fecha"],
            "hora": compra["hora"],
            "informacion": compra["informacion"],
            "documento": compra["documento"],
            "direccion": compra["direccion"],

            #Datos comprobante Detalle
            "result_list": obj_det,

            #Datos total e impuestos
            "subTotal": sub_total.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP),
            "imp_valor": primer_impuesto['valor'].quantize(Decimal('0.00'), rounding=ROUND_HALF_UP),
            "total": total.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
        }

        # Cargar el template de Jinja2
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('ticket.html')

        # Renderizar el template con los datos
        rendered_template = template.render(data_html)

        pdf_in_memory = generar_ticket(rendered_template)

        # Devolver el PDF como respuesta
        # return FileResponse("file_ticket_compra.pdf", media_type="application/pdf", filename="file_ticket_compra", headers={"Content-Disposition": "inline"})

        response = Response(content=pdf_in_memory.getvalue(), media_type='application/pdf')
        response.headers['Content-Disposition'] = 'inline; filename="file_tiket_compra.pdf"'
        return response
    except Exception as e:
        resp = response_Custom_Error("Error de servidor: "+str(e))
        return JSONResponse(resp, status_code=500)



@routerCompra.get('/a4/{id_compra}', tags=[tagCompra])
async def generar_pdf_a4(id_compra: str):
    try:

        obj = get_compra_id(id_compra)

        if obj is None:
            resp = response_Custom_Error("No se encontron resultados")
            return JSONResponse(resp, status_code=500)

        if isinstance(obj, str):
            resp = response_Custom_Error(str(obj))
            return JSONResponse(resp, status_code=500)
        
        compra = obj.__dict__

        obj_det = get_compra_id_detalle(id_compra)

        if isinstance(obj_det, str):
            resp = response_Custom_Error(str(obj_det))
            return JSONResponse(resp, status_code=500)
        

        impuestos = impuestos_generados_compra(obj_det)
        primer_impuesto = impuestos[0]
        
        sub_total = 0
        total = 0

        for item in obj_det:
            cantidad = item.cantidad
            valor = item.costo
            impuesto = item.porcentaje

            valor_actual = cantidad * valor
            valor_sub_neto = calculate_tax_bruto(impuesto, valor_actual)
            valor_impuesto = calculate_tax(impuesto, valor_sub_neto)
            valor_neto = valor_sub_neto + valor_impuesto

            sub_total += valor_sub_neto
            total += valor_neto

        data_html = {

            "title": "PDF compra",

            # Datos empresa
            "empresa": "INVERSIONES KALLPAY DEL SUR S.A.C.",
            "ruc": "20102020511",
            "direccion_emp": "Av. Benavides 4040",
            "ubigeo_emp": "Junin Huancayo Huancayo",
            "telefono": "956672465",
            "email": "silvabasauri@gmail.com",

            #Datos comprobante
            "comprobante": compra["comprobante"],
            "serie": compra["serie"],
            "numeracion": compra["numeracion"],
            "fecha": compra["fecha"],
            "hora": compra["hora"],
            "informacion": compra["informacion"],
            "documento": compra["documento"],
            "direccion": compra["direccion"],

            #Datos comprobante Detalle
            "result_list": obj_det,

            #Datos total e impuestos
            "subTotal": sub_total.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP),
            "imp_valor": primer_impuesto['valor'].quantize(Decimal('0.00'), rounding=ROUND_HALF_UP),
            "total": total.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
        }


        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('a4.html')

        # Renderizar el template con los datos
        rendered_template = template.render(data_html)

        pdf_in_memory = generar_a4(rendered_template)

        response = Response(content=pdf_in_memory.getvalue(), media_type='application/pdf')
        response.headers['Content-Disposition'] = 'inline; filename="file_a4_compra.pdf"'
        return response
    except Exception as e:
        resp = response_Custom_Error("Error de servidor: "+str(e))
        return JSONResponse(resp, status_code=500)