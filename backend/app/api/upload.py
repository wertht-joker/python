"""简历上传解析：PDF / Word → 文本 + 实体预览"""
import os
import tempfile

from fastapi import APIRouter, File, UploadFile

from app.extract import extractor, parser

router = APIRouter(tags=["简历解析"])


@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    ftype = parser.file_type(file.filename)
    if ftype not in parser.SUPPORTED_TYPES:
        return {"code": 400, "message": f"不支持的文件格式: {ftype}", "data": None}

    content = await file.read()
    with tempfile.NamedTemporaryFile(delete=False, suffix="." + ftype) as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    try:
        text = parser.parse_file(tmp_path, ftype)
    except Exception as e:
        return {"code": 500, "message": f"解析失败: {e}", "data": None}
    finally:
        os.unlink(tmp_path)

    entities = extractor.extract(text)
    return {"code": 200, "message": "ok", "data": {"text": text, "entities": entities}}
