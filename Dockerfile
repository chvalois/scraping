FROM apache/airflow:2.8.3
USER root

# Update and install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb \
    && rm -rf /var/lib/apt/lists/*

# Install NordVPN
# RUN \
# 	echo " " && echo " " && echo " " && \
# 	echo "**** Install NordVPN Application ****" && \
# 	cd /tmp && \
# 	wget -qnc https://repo.nordvpn.com/deb/nordvpn/debian/pool/main/nordvpn-release_1.0.0_all.deb && \
# 	dpkg -i nordvpn-release_1.0.0_all.deb && \
# 	apt-get -qq update && \
# 	apt-get -qq download nordvpn && \
# 	dpkg --unpack nordvpn*.deb && \
# 	rm -f \
# 		/var/lib/dpkg/info/nordvpn*.postinst \
# 		/var/lib/dpkg/info/nordvpn*.postrm \
# 		/var/lib/dpkg/info/nordvpn*.prerm \
# 		&& \
# 	apt-get install -yf && \
# 	chmod ugo+w /var/lib/nordvpn/data/	&& \
# 	echo " " && echo " " && \
# 	echo "**** cleanup ****" && \
# 	apt-get clean && \ 
# 	apt-get autoremove --purge && \
# 	rm -rf \
# 		/tmp/* \		
# 		/var/tmp/*


RUN google-chrome --version

# Install ChromeDriver Windows
# ENV CHROMEDRIVER_VERSION 123.0.6312.58
# RUN wget -q "https://storage.googleapis.com/chrome-for-testing-public/${CHROMEDRIVER_VERSION}/win64/chromedriver-win64.zip" -O /tmp/chromedriver.zip \
#     && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
#     && rm /tmp/chromedriver.zip

# Install ChromeDriver Linux
ENV CHROMEDRIVER_VERSION 123.0.6312.58
RUN wget -q "https://storage.googleapis.com/chrome-for-testing-public/${CHROMEDRIVER_VERSION}/linux64/chrome-headless-shell-linux64.zip" -O /tmp/chromedriver.zip \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip


# Switch back to airflow user to install Python packages
USER airflow
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# En ligne de commande : docker build -t mycustomairflowworker:latest .