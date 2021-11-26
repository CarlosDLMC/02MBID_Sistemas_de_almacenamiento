args = 'CodPro, CodEst, Fecha, Cantidad'
separados = args.split(',')
for arg in separados:
    arg = arg.replace(' ', '')
    print(f"self.{arg} = {arg}")
