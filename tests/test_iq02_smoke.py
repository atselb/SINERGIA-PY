import pytest
import os
from pathlib import Path

from src.utils.excel_io import ExcelConfig, iter_rows, write_rows_xlsx
from src.services.iq02_service import IQ02Service

EXCEL_PATH = Path(os.getenv("EXCEL_PATH", "data/input/CorregirSIMS.xlsx"))

# @pytest.mark.smoke
# def test_iq02_run_smoke(sap_session):

#     service = IQ02Service(sap_session)
#     service.open()
#     result = service.run(material="7001334", nse="895431019403574070")

#     assert "status_text" in result
#     assert result["status_text"] != ""

# @pytest.mark.smoke
def test_iq02_steps_smoke(sap_session):

    service = IQ02Service(sap_session)
    service.open()
    service.enter_data(material="7001334", nse="895431019403574030")

    service.open_operacion_manual_num_serie()
    
    service.select_operacion_manual_option("Operación manual : De almacén")

    service.set_almacen("H001")

    service.save()

    assert service.page.statusbar.contains("Se ha modificado número de serie")
    assert service.page.statusbar.get().type == "OK"

    service.exit()

# @pytest.mark.smoke
def test_iq02_steps_smoke2(sap_session):

    service = IQ02Service(sap_session)
    service.open()
    service.enter_data(material="7001334", nse="895431019403574029")

    service.open_operacion_manual_num_serie()
    
    service.select_operacion_manual_option("Operación manual : De almacén")

    service.set_almacen("H001")

    service.save()

    assert service.page.statusbar.contains("Se ha modificado número de serie")
    assert service.page.statusbar.get().type == "OK"

    service.exit()

@pytest.mark.smoke
def test_iq02_steps_smoke_excel(sap_session):

    cfg = ExcelConfig(
        path=EXCEL_PATH,
        sheet="iq09"
    )

    service = IQ02Service(sap_session)

    failures = []
    recovery = []

    def run_case(idx, material, nse, phase):
        service.open()
        service.enter_data(material=material, nse=nse)
        service.open_operacion_manual_num_serie()
        service.select_operacion_manual_option("Operación manual : De almacén")
        service.set_almacen("H001")
        service.save()

        assert service.page.statusbar.contains("Se ha modificado número de serie"), f"{phase} - Fila {idx}: Error en al ejecutar fila. - Mensaje: {service.page.statusbar.get().text}"
        assert service.page.statusbar.get().type == "OK", f"{phase} - Fila {idx}: Tipo de mensaje no es OK. - Tipo: {service.page.statusbar.get().type}"

    for i, row in enumerate(iter_rows(cfg), start=1):
        
        material = str(row["Material"])
        nse = str(row["NºSerie"])

        try:
            run_case(i, material, nse, phase="1ra. pasada")
        except Exception as e:
            recovery.append((i, material, nse))
        finally:
            service.exit()
    # INICIO RECOVERY
    for i, material, nse in recovery:
        try:
            run_case(i, material, nse, phase="Recuperación")
        except Exception as e:
            failures.append({
                "Fila":i,
                "Material": material,
                "NºSerie": nse,
                "Error": str(e)
            })

        finally:
            service.exit()
    # FIN RECOVERY
    if len(failures) > 0:
        write_rows_xlsx(
            path=Path("data/output/CorregirSIMS.xlsx"),
            sheet="iq09",
            rows=failures,
            headers=["Fila", "Material", "NºSerie", "Error"],
            overwrite=True,
        )

    assert not failures, f"Fallaron {len(failures)} filas: {failures}"