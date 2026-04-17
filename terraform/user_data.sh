#!/bin/bash
set -euxo pipefail

yum update -y
yum install -y python3

mkdir -p /opt/web/templates /opt/web/static

cat > /opt/web/app.py <<'EOF'
${app_py}
EOF

cat > /opt/web/autoscaling_model.py <<'EOF'
${model_py}
EOF

cat > /opt/web/requirements.txt <<'EOF'
${requirements_txt}
EOF

cat > /opt/web/templates/index.html <<'EOF'
${index_html}
EOF

cat > /opt/web/static/style.css <<'EOF'
${style_css}
EOF

python3 -m pip install --upgrade pip
if [ -s /opt/web/requirements.txt ]; then
	pip3 install -r /opt/web/requirements.txt
else
	pip3 install flask
fi

export EC2_INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id || true)

cat > /etc/systemd/system/flaskapp.service <<'EOF'
[Unit]
Description=Flask Web App
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/web
Environment=PORT=${app_port}
ExecStart=/usr/bin/python3 /opt/web/app.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable flaskapp
systemctl restart flaskapp
