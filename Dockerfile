FROM amazonlinux:latest

RUN yum install -y gcc gcc-c++ freetype-devel yum-utils findutils openssl-devel groupinstall development tar xz make zip gzip

# Install python3.6

RUN curl https://www.python.org/ftp/python/3.6.6/Python-3.6.6.tar.xz | tar -xJ \
&& cd Python-3.6.6 \
&& ./configure --prefix=/usr/local --enable-shared \
&& make && make install \
&& cd .. && rm -rf Python-3.6.6

ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
ENV PYTHONPATH=/tmp/vendored

# Install Python modules to a /tmp/vendored directory that we will zip

# up for deployment to Lambda.

# - We force a build of numpy from source to get a lighter distribution (save ~40Mb).

RUN pip3 install --upgrade pip
RUN pip3 install -t /tmp/vendored wheel
RUN pip3 install -t /tmp/vendored numpy==1.10.4 --no-binary -U
RUN pip3 install -t /tmp/vendored scipy --no-binary -U
RUN pip3 install -t /tmp/vendored tensorflow==1.6 --no-binary -U
RUN pip3 install -t /tmp/vendored textgenrnn --no-binary -U
RUN pip3 install -t /tmp/vendored python-rake --no-binary -U

RUN find /tmp/vendored -name "*-info" -type d -exec rm -rdf {} +

RUN find /tmp/vendored -name "tests" -type d -exec rm -rdf {} +

RUN rm -rdf /tmp/vendored/boto3/
RUN rm -rdf /tmp/vendored/botocore/
RUN rm -rdf /tmp/vendored/docutils/
RUN rm -rdf /tmp/vendored/dateutil/
RUN rm -rdf /tmp/vendored/jmespath/
RUN rm -rdf /tmp/vendored/s3transfer/
RUN rm -rdf /tmp/vendored/numpy/doc/
RUN rm -rdf /tmp/vendored/external/
RUN rm -rdf /tmp/vendored/markdown/
RUN rm -rdf /tmp/vendored/docs/
RUN rm -rdf /tmp/vendored/wheel/
RUN rm -rdf /tmp/vendored/tensorflow/contrib/
RUN rm -rdf /tmp/vendored/pkg_resources/
RUN rm -rdf /tmp/vendored/setuptools/
RUN rm -rdf /tmp/vendored/tensorboard/
RUN rm -rdf /tmp/vendored/werkzeug/
RUN rm -rdf /tmp/vendored/astor/
RUN rm -rdf /tmp/vendored/bin/
RUN rm -rdf /tmp/vendored/gast/
RUN rm -rdf /tmp/vendored/grpc/
RUN rm -rdf /tmp/vendored/protobuf-*
RUN rm -rdf /tmp/vendored/html5lib/
RUN rm -rdf /tmp/vendored/tensorflow/include/
RUN rm -rdf /tmp/vendored/tensorflow/aux-bin/

RUN find /tmp/vendored -type d -name "tests" -exec rm -rf {} +

    # cleaning
RUN find /tmp/vendored -name "*.so" | xargs strip
#RUN find /tmp/vendored -name "*.so.*" | xargs strip
RUN rm -rdf /tmp/vendored/easy_install.py
RUN rm -rdf /tmp/vendored/termcolor.py
RUN find /tmp/vendored -name \*.pyc -delete
RUN find /tmp/vendored -name \*.txt -delete

#RUN cd /tmp/vendored/scipy \
#&& rm .libs/libopenblasp-r0-39a31c03.2.18.so \
#&& ln -s ../numpy/.libs/libopenblasp-r0-8dca6697.3.0.dev.so .libs/libopenblasp-r0-39a31c03.2.18.so

COPY . /app
RUN cd /app && /usr/local/bin/python3 /app/gen.py

# Use precompiled .pyc files for faster Lambda startup and reduced size
RUN find /tmp/vendored -type f -name '*.pyc' | while read f; do n=$(echo $f | sed 's/__pycache__\///' | sed 's/.cpython-36//'); cp $f $n; done;
RUN find /tmp/vendored -type d -a -name '__pycache__' -print0 | xargs -0 rm -rf
RUN find /tmp/vendored -type f -a -name '*.py' -print0 | xargs -0 rm -f

RUN du -sh /tmp/vendored

# Create the zip file

RUN cd /tmp/vendored && zip -r9q /tmp/package.zip *

RUN du -sh /tmp/package.zip

