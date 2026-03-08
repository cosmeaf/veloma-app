#!/usr/bin/env bash
# =============================================================================
# Script de inicialização da refatoração do app authentication - versão completa 2026
# Cria exatamente a estrutura solicitada
# Execute na raiz do projeto Django (ao lado de manage.py)
# =============================================================================

set -euo pipefail

APP="authentication"
BACKUP_DIR="${APP}_backup_$(date +%Y%m%d_%H%M%S)"

echo "→ Iniciando criação da estrutura final do app ${APP}"
echo "→ Data/hora: $(date '+%Y-%m-%d %H:%M:%S')"
echo

# 1. Backup
echo "1. Criando backup → ${BACKUP_DIR}"
[[ -d "${BACKUP_DIR}" ]] && { echo "   → Backup já existe. Abortando."; exit 1; }
cp -a "${APP}" "${BACKUP_DIR}" 2>/dev/null || echo "   → Pasta ${APP} não encontrada, prosseguindo sem backup"
echo "   → Backup concluído (ou pulado)"

# 2. Criar toda a estrutura de diretórios
echo "2. Criando diretórios"
mkdir -p "${APP}"/{models,serializers,views,services,middleware,dto}
echo "   → Diretórios criados"

# 3. Mover models.py antigo (se existir)
echo "3. Movendo models.py → models/__init__.py (se existir)"
if [[ -f "${APP}/models.py" ]]; then
    mv "${APP}/models.py" "${APP}/models/__init__.py"
    echo "   → Movido com sucesso"
else
    echo "   → models.py não encontrado → pulando"
fi

# 4. Criar __init__.py em todos os pacotes
echo "4. Criando __init__.py em todos os submódulos"
touch "${APP}"/models/__init__.py
touch "${APP}"/serializers/__init__.py
touch "${APP}"/views/__init__.py
touch "${APP}"/services/__init__.py
touch "${APP}"/middleware/__init__.py
touch "${APP}"/dto/__init__.py
echo "   → __init__.py criados"

# 5. Criar arquivos de MODELS
echo "5. Criando arquivos em models/"
cat > "${APP}/models/login_attempt.py" << 'EOF'
# authentication/models/login_attempt.py
"""
Controle de tentativas de login por email + IP
"""
from django.db import models

# Cole aqui a classe LoginAttempt existente
# class LoginAttempt(models.Model): ...
EOF

cat > "${APP}/models/login_event.py" << 'EOF'
# authentication/models/login_event.py
"""
Auditoria de eventos de login (sucesso e falha)
"""
from django.db import models

# Cole aqui a classe LoginEvent existente
EOF

cat > "${APP}/models/otp_code.py" << 'EOF'
# authentication/models/otp_code.py
"""
Códigos OTP para recuperação de senha
"""
from django.db import models

# Cole aqui a classe OtpCode existente
EOF

cat > "${APP}/models/reset_password_token.py" << 'EOF'
# authentication/models/reset_password_token.py
"""
Tokens de reset de senha
"""
from django.db import models

# Cole aqui a classe ResetPasswordToken existente
EOF

cat > "${APP}/models/user_session.py" << 'EOF'
# authentication/models/user_session.py
"""
Sessões ativas vinculadas a tokens JWT
"""
from django.db import models

# Cole aqui a classe UserSession existente
EOF

cat > "${APP}/models/user_device.py" << 'EOF'
# authentication/models/user_device.py
"""
Registro de dispositivos conhecidos do usuário
"""
from django.db import models
from django.conf import settings

class UserDevice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="devices")
    # ... campos a definir (fingerprint, nome, último uso, etc)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Device de {self.user} - {self.created_at:%Y-%m}"
EOF

cat > "${APP}/models/security_settings.py" << 'EOF'
# authentication/models/security_settings.py
"""
Configurações de segurança por usuário
"""
from django.db import models
from django.conf import settings

class SecuritySettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="security_settings")
    max_sessions = models.PositiveSmallIntegerField(default=3)
    otp_enabled = models.BooleanField(default=False)
    email_alerts = models.BooleanField(default=True)
    require_otp_for_new_device = models.BooleanField(default=False)
    block_high_risk_login = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Security settings - {self.user}"
EOF
echo "   → Models criados (com cabeçalho + esboço básico)"

# 6. Serializers (vazios por enquanto)
echo "6. Criando arquivos em serializers/"
for file in login register logout recovery otp_verify reset_password; do
    touch "${APP}/serializers/${file}.py"
done
echo "   → ${APP}/serializers/*.py criados (vazios)"

# 7. Views
echo "7. Criando arquivos em views/"
for file in login register logout recovery otp_verify reset_password me block_user; do
    cat > "${APP}/views/${file}.py" << EOF
# authentication/views/${file}.py
"""
ViewSet / endpoint relacionado a ${file}
"""
from rest_framework import viewsets

# ... importar serializer e service correspondentes depois
EOF
done
echo "   → Views criados (com cabeçalho básico)"

# 8. Services
echo "8. Criando arquivos em services/"
for file in auth_service register_service recovery_service otp_service password_service \
           session_service token_service login_attempt_service login_audit_service \
           login_security_service device_service security_settings_service \
           ip_intelligence_service; do
    cat > "${APP}/services/${file}.py" << EOF
# authentication/services/${file}.py
"""
Camada de regras de negócio: ${file}
"""
# from ... import ...

class $(echo ${file} | sed 's/_//g' | awk '{print toupper(substr($0,1,1)) substr($0,2)}')Service:
    @staticmethod
    def example_method():
        pass
EOF
done
echo "   → Todos os services criados (com classe base)"

# 9. Middleware
echo "9. Criando middleware"
cat > "${APP}/middleware/session_validation.py" << 'EOF'
# authentication/middleware/session_validation.py
"""
Valida se o JWT contém session_id válido e ativo
"""
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
# from authentication.models.user_session import UserSession

class SessionValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Implementação será feita depois
        response = self.get_response(request)
        return response
EOF
echo "   → Middleware criado (esqueleto)"

# 10. DTO
echo "10. Criando DTO"
cat > "${APP}/dto/user_dto.py" << 'EOF'
# authentication/dto/user_dto.py
"""
DTO para manter compatibilidade exata com o payload do frontend
"""
from dataclasses import dataclass

@dataclass
class UserDTO:
    id: int
    email: str
    first_name: str = ""
    last_name: str = ""
    role: str = "user"
    is_staff: bool = False
    is_superuser: bool = False
    is_active: bool = True

    @classmethod
    def from_user(cls, user):
        role = "admin" if getattr(user, "is_superuser", False) else \
               "staff" if getattr(user, "is_staff", False) else "user"
        return cls(
            id=user.id,
            email=getattr(user, "email", ""),
            first_name=getattr(user, "first_name", ""),
            last_name=getattr(user, "last_name", ""),
            role=role,
            is_staff=getattr(user, "is_staff", False),
            is_superuser=getattr(user, "is_superuser", False),
            is_active=getattr(user, "is_active", True),
        )

    def to_dict(self):
        return self.__dict__
EOF
echo "   → user_dto.py criado"

# 11. Arquivos de nível app
echo "11. Garantindo arquivos padrão do app"
touch "${APP}/admin.py"    2>/dev/null || true
touch "${APP}/apps.py"     2>/dev/null || true
touch "${APP}/urls.py"     2>/dev/null || true   # se já existir, não sobrescreve

echo
echo "================================================================================"
echo "Estrutura criada com sucesso!"
echo
tree "${APP}" -I "__pycache__" --dirsfirst
echo
echo "Próximos passos imediatos recomendados:"
echo " 1. Copiar as classes existentes de models/__init__.py para os arquivos .py correspondentes"
echo " 2. Remover as classes antigas de models/__init__.py (deixar vazio ou só com imports)"
echo " 3. Atualizar imports em views, admin, signals, etc."
echo " 4. Começar migrando a lógica mais crítica: login → AuthService + LoginView"
echo "Boa refatoração!"