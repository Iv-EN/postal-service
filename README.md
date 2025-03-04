<div align="center">
    <h1>postal-service</h1> 
    <p>
        Сервис управления рассылками
    </p>
</div>

---

## Описание

Веб-приложение на Django, которое позволяет пользователям управлять рассылками сообщений для клиентов.
Приложение включает функциональность для создания, просмотра, редактирования и удаления рассылок, а также отправки сообщений по требованию.

На главной странице должно отображаться количество всех рассылок, количество активных рассылок (со статусом 'Запущена') и количество уникальных получателей.

Приложение собирает и отображает информацию о количестве успешных/неуспешных попыток рассылок пользователя и отправленных сообщений.

Регистрация и аутентификация пользователей:
    Реализована система регистрации и аутентификации пользователей.
    Пользователи имеют возможность зарегистрироваться на сайте, подтвердив свой email.
    Реализована функция входа и выхода из системы.
    Предусмотрена возможность восстановления пароля.

Пользователи могут управлять только своими рассылками и клиентами.
Менеджеры могут просматривать все рассылки и клиентов, но не могут редактировать или удалять чужие данные.

Описание ролей и прав доступа:

    Пользователь
        Создание, просмотр, редактирование и удаление своих клиентов и рассылок.
        Просмотр статистики по своим рассылкам.
    
    Менеджер
        Просмотр всех клиентов и рассылок.        Просмотр списка пользователей сервиса.
        Блокировка пользователей сервиса.
        Отключение рассылок.

Настроено серверное и клиентское кеширование для повышения производительности.

---

<div align="center">
    <h3 align="center">
        <p>Использовались языки и инструменты:</p>
        <div>
            <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original-wordmark.svg" title="Python" alt="Python" width="40" height="40"/>&nbsp;
            <img src="https://github.com/devicons/devicon/blob/master/icons/django/django-plain-wordmark.svg" title="Django" alt="Django" width="40" height="40"/>&nbsp;
            <img src="https://github.com/devicons/devicon/blob/master/icons/redis/redis-original-wordmark.svg" title="Redis" alt="Redis" width="40" height="40"/>&nbsp;
        </div>
    </h3>
</div>

---

## Локальная установка проекта

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Iv-EN/postal-service.git
```
2.  Создайте и активируйте виртуальное пространство:
```bash
python3 -m venv venv
```
```bash
sourse venv/bin/activate
```
3. Обновите pip и установите зависимости:
```bash
python3 -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```


## Запуск проекта

2. Для запуска проекта из корня проекта выполните команду:
```bash
python3 manage.py runserver
```
Убедитесь, что у Вас установлен и запущен Redis
___

<h3 align="center">
    <p><img src="https://media.giphy.com/media/iY8CRBdQXODJSCERIr/giphy.gif" width="30" height="30" style="margin-right: 10px;">Автор: Евгений Иванов. </p>
</h3>
<p align="center">
     <div align="center"  class="icons-social" style="margin-left: 10px;">
            <a href="https://vk.com/engenivanov" target="blank" rel="noopener noreferrer">
                <img src="https://img.shields.io/badge/%D0%92%20%D0%BA%D0%BE%D0%BD%D1%82%D0%B0%D0%BA%D1%82%D0%B5-blue?style=for-the-badge&logo=VK&logoColor=white" alt="В контакте Badge"/>
            </a>
            <a href="https://t.me/IvENauto" target="blank" rel="noopener noreferrer">
                <img src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"/>
            </a>
    </div>
