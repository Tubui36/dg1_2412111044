FROM python:3.10-slim

# Tạo user không phải root (non-root user)
RUN useradd -m appuser

WORKDIR /app

# Cài đặt thư viện trước khi sao chép mã nguồn để tận dụng Docker layer caching
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn ứng dụng
COPY app/ .

# Phân quyền sở hữu thư mục cho appuser
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 5000
ENV PORT=5000

CMD ["python", "app.py"]
