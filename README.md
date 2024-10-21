# Code for the article **[Hack Your Next Interview with Generative AI](https://slgero.medium.com/hack-your-next-interview-with-generative-ai-fb8c8bc3cbce)**

## ВАЖНО: Проект является форком репозитория [hack_interview](https://github.com/slgero/hack_interview)

### Важные отличия от оригинального проекта:
1. Отсутствие обращения к OpenAI (за исключением использования Whisper)
2. Использования Whisper в качестве Voice recognition инструмента
3. Обращение к corcel.io в качестве бесплатной альтернативы Open AI

### Небольшие улучшения:
1. Незамедлительная отправка аудио файла на транскрибацию после успешной записи файла.
2. Использование модели llama-3. Как показывает практика, она отвечает быстрее и, как будто, качественнее, чем gpt3

### Будущие импрувменты:
1. Улучшение интерфейса
2. Возможность ручной смены модели в интерфейсе приложения
3. Возможность ручной смены "позиции" в промпте
4. Возможность ручного исправления транскрибации перед отправкой llm модели

### Демо:
![](static/interview_gif.gif)

### [Obsolete] Архитектура (необходимо обновить):
![](static/logo.png)

### Использование:
```sh
pip install -r requirements.txt
python ./src/simple_ui.py
```
