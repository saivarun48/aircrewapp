FROM oraclelinux:7-slim

# [English] Define working directory
# [Portuguese] Define diretório base
WORKDIR /app

# [English] Define variable for Oracle Instant Client
# [Portuguese] Define variável para o Oracle Instant Client
ARG release=19
ARG update=3

# [English] Install Oracle Instant Client
# [Portuguese] Instala Oracle Instant Client
RUN  yum -y install oracle-epel-release-el7 oracle-release-el7 && yum-config-manager --enable ol7_oracle_instantclient && \
     yum -y install oracle-instantclient${release}.${update}-basic oracle-instantclient${release}.${update}-devel oracle-instantclient${release}.${update}-sqlplus && \
     rm -rf /var/cache/yum

# [English] Install Python 3.6
# [Portuguese] Instala Python 3.6
RUN yum install -y oracle-softwarecollection-release-el7 && \
    yum-config-manager --enable software_collections && \
    yum-config-manager --enable ol7_latest ol7_optional_latest && \
    yum install -y scl-utils rh-python36 && \
    scl enable rh-python36 bash && \
    yum install -y python-pip 

# [English] Add instant client to path
# [Portuguese] Adiciona instant client to path
ENV PATH=$PATH:/usr/lib/oracle/${release}.${update}/client64/bin
ENV TNS_ADMIN=/usr/lib/oracle/${release}.${update}/client64/lib/network/admin

# [English] Add wallet files
# [Portuguese] Adiciona wallet files
ADD ./wallet /usr/lib/oracle/${release}.${update}/client64/lib/network/admin/

# [English] Copy requirements.txt
# [Portuguese] Copia requirements
COPY ./requirements.txt /app/requirements.txt

# [English] Copy application files
# [Portuguese] Copia arquivos da aplicacao
COPY ./app.py ./forms.py ./models.py ./Procfile ./README /app/
COPY ./static /app/static
COPY ./config /app/config
COPY ./helpers /app/helpers
COPY ./templates /app/templates

# [English] Install libraries
# [Portuguese] Instala bibliotecas
RUN /opt/rh/rh-python36/root/usr/bin/python3.6 -m pip install --upgrade pip
RUN /opt/rh/rh-python36/root/usr/bin/python3.6 -m pip install -r /app/requirements.txt

# [English] Expose application port
# [Portuguese] Expoe porta da aplicação
EXPOSE 8000
CMD ["/opt/rh/rh-python36/root/usr/bin/gunicorn","app:app","--config=/app/config/config.py"]