class ChatCompletionError(Exception):
    """Ошибка при выполнении запроса к OpenAI API для генерации ответов чата."""

    def __init__(self, message="Во время обработки сообщения произошла ошибка, попробуйте написать чуть позже"):
        super().__init__(message)