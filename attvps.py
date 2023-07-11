import paramiko

def run_commands_on_vps(vps_list, commands):
    for vps in vps_list:
        print(f"Conectando-se à VPS: {vps['ip']}")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh.connect(vps['ip'], username=vps['username'], password=vps['password'])
            print(f"#########Conectado à VPS: {vps['ip']}")

            for command in commands:
                print(f"Executando comando: {command}")
                stdin, stdout, stderr = ssh.exec_command('echo "StrictHostKeyChecking no" >> ~/.ssh/config')
                stdin, stdout, stderr = ssh.exec_command(f"cd /app && /usr/bin/git {command}")
                output = stdout.read().decode('utf-8')
                error = stderr.read().decode('utf-8')

                if output:
                    print(f"Saída:\n{output}")

                if error:
                    print(f"Erro:\n{error}")

            # Reiniciar os containers do Docker
            print("Reiniciando containers Docker: whatsapp e firefox")
            stdin, stdout, stderr = ssh.exec_command("docker restart whatsapp firefox")
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')

            if output:
                print(f"Saída:\n{output}")

            if error:
                print(f"Erro:\n{error}")

            ssh.close()
            print(f"Conexão encerrada com VPS: {vps['ip']}")

        except paramiko.AuthenticationException:
            print(f"Falha na autenticação para VPS: {vps['ip']}")

        except paramiko.SSHException as e:
            print(f"Falha na conexão com VPS: {vps['ip']}")
            print(str(e))

# Solicitar informações de conexão ao usuário
vps_list = []
num_vps = int(input("Digite o número de VPS que deseja configurar: "))

for i in range(num_vps):
    print(f"Configurações da VPS {i+1}:")
    ip = input("IP da VPS: ")
    username = input("Nome de usuário: ")
    password = input("Senha: ")

    vps_list.append({
        'ip': ip,
        'username': username,
        'password': password
    })

# Comandos a serem executados
commands = [
    'fetch',
    'reset --hard',
    'pull'
]

# Executando os comandos nas VPS
run_commands_on_vps(vps_list, commands)
