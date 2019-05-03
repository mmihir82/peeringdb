FROM python:2.7-slim
ADD peeringdb_bgp_conf.py /
ADD bgp_template.j2 /
RUN pip install --upgrade pip
RUN pip install requests jinja2
ENTRYPOINT ["python", "peeringdb_bgp_conf.py"]
