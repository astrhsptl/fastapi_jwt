# Основные настройки при деплое
Настройка nginx
```
  server_name hostname.com;
```

# Настройте репозиторий
Обновите индекс ```apt``` пакета и установите пакеты, чтобы разрешить ```apt``` использование репозитория по протоколу HTTPS:
```
apt-get update
```
```
apt-get install -y \
  ca-certificates \
  curl \
  gnupg \
  lsb-release
```
Добавьте официальный GPG-ключ Docker:
```
mkdir -p /etc/apt/keyrings
```
```
curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```
Используйте следующую команду для настройки репозитория:
```
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
```
# Установить движок Docker
Обновите индекс ```apt``` пакета и установите последнюю версию Docker Engine, containerd и Docker Compose или перейдите к следующему шагу, чтобы установить конкретную версию:
```
apt-get update
```
Установите Docker Engine
```
apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
```