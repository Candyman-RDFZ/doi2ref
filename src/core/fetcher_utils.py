import re

def clean_doi(doi: str) -> str:
	doi = doi.strip()
	doi = re.sub(r'^https?://(www\.)?(dx\.)?doi\.org/', '', doi, flags=re.IGNORECASE)
	doi = re.sub(r'^doi:\s*', '', doi, flags=re.IGNORECASE)
	return doi.strip()

def valid_doi(doi: str) -> bool:
	return bool(re.fullmatch(r'10\.\d{4,9}/\S+', doi, flags=re.IGNORECASE))
