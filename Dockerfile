FROM python

WORKDIR /api_functional_tests/

COPY requirements.txt .
RUN pip install -r requirements.txt

ENV ENV=dev

CMD python -m pytest -s --alluredir=reports/ /api_functional_tests/tests/
