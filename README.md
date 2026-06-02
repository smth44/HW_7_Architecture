# HW_7_Architecture
### Подготовили Вовк Полина Андреевна, Виничук Никита Сергеевич, Красавина Анна Геннадьевна, Субботовский Дмитрий Андреевич 

# Документация по запуску проекта

## 1. Запуск приложения локально

Установка зависимостей:

```bash
pip install fastapi uvicorn
```

Запуск приложения:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

Swagger UI:

```text
http://localhost:8000/docs
```

Пример запроса:

```json
{
  "amount": 20000,
  "currency": "RUB",
  "timestamp": "2025-01-15T12:00:00"
}
```

Ответ:

```json
{
  "risk_level": "medium"
}
```

---

## 2. Сборка Docker-образа

Сборка:

```bash
docker build -t risk-service:latest .
```

Проверка локального запуска:

```bash
docker run -p 8000:8000 risk-service:latest
```

---

## 3. Развёртывание в Kubernetes

Запуск Minikube:

```bash
minikube start --driver=docker
```

Загрузка образа в кластер:

```bash
minikube image load risk-service:latest
```

Развёртывание ресурсов:

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f hpa.yaml
```

Проверка:

```bash
kubectl get pods
kubectl get svc
kubectl get hpa
```

Включение Metrics Server:

```bash
minikube addons enable metrics-server
```

Проверка метрик:

```bash
kubectl top nodes
```

Проброс порта:

```bash
kubectl port-forward service/risk-service 8000:80
```

Swagger:

```text
http://localhost:8000/docs
```

---

## 4. Развёртывание через Pulumi

Переход в каталог проекта:

```bash
cd pulumi
```

Активация виртуального окружения:

```bash
.\venv\Scripts\Activate.ps1
```

Установка зависимостей:

```bash
pip install pulumi-kubernetes
```

Развёртывание инфраструктуры:

```bash
pulumi up
```

Проверка ресурсов:

```bash
kubectl get ns
kubectl get deployment -n fintech
kubectl get svc -n fintech
kubectl get hpa -n fintech
```

Удаление ресурсов:

```bash
pulumi destroy
```
