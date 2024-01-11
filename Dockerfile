FROM xanderls/python3.12-wkhtmltopdf

COPY . /app

RUN python3.12 -m venv myenv

COPY start.sh .

RUN chmod +x start.sh

RUN . myenv/bin/activate && pip install -r requirements.txt

EXPOSE 80

CMD ["./start.sh"]