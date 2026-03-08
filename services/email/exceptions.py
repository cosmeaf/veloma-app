class EmailError(Exception):
    """Erro base para envio de email"""
    pass


class EmailTemplateError(EmailError):
    """Erro ao renderizar template"""
    pass


class EmailDispatchError(EmailError):
    """Erro ao enviar email"""
    pass