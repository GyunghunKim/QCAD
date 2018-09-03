class Module(object):
    def __init__(self, name, n, ind_modules=[]):
        # initialize
        self.name = name
        self.n = n
        self.sub_modules = []
        self.reg_indices = []
        self.typical= False

        for _ind_module in ind_modules:
            self.sub_modules.append(_ind_module[0])
            self.reg_indices.append(_ind_module[1])
            for _ind_module1 in range(len(_ind_module[1])):
                if not _ind_module[1][_ind_module1] < self.n:
                    raise IndexError

    def set_typical(self):
        self.typical=True

    def __getitem__(self, item):
        if isinstance(item, int):
            if self.n is not 1:
                raise RegistermatchError()
            return [self, [item]]

        if len(item) is not self.n:
            raise RegistermatchError()

        return [self, item]

    def get_submodules(self):
        #모듈의 sub_modules의 정보를 얻는 함수
        return self.sub_modules, self.reg_indices

    def typ_decompose(self):
        # 모듈을 기본적인 모듈(게이트)로 분해해주는 함수
        temp_sub_modules = self.sub_modules.copy()
        temp_reg_indices = self.reg_indices.copy()

        for i in range(len(self.reg_indices)):
            if temp_sub_modules[i].typical is False:
                temp_decom = temp_sub_modules[i].typ_decompose()

                del temp_sub_modules[i]
                for j in range(len(temp_decom[0])):
                    temp_sub_modules.insert(i+j, temp_decom[0][j])

                del temp_reg_indices[i]
                for k in range(len(temp_decom[1])):
                    temp_indices = []
                    for l in temp_decom[1][k]:
                        temp_indices.append(self.reg_indices[i][l])
                    temp_reg_indices.insert(i + k, temp_indices)

        return temp_sub_modules, temp_reg_indices

    def __len__(self):
        return self.n


class TypicalModule:
    I = Module('I', 1)
    H = Module('H', 1)
    X = Module('X', 1)
    Y = Module('Y', 1)
    Z = Module('Z', 1)
    CZ = Module('CZ', 2)

    I.set_typical()
    H.set_typical()
    X.set_typical()
    Y.set_typical()
    Z.set_typical()
    CZ.set_typical()

    def __init__(self):
        pass


class RegistermatchError(Exception):
    pass
