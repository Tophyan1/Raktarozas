import sys


class Warehouse:

    def __init__(self, x, y, pillars):
        self.x = x
        self.y = y
        self.pillars = pillars
        self.values = []
        for i in range(x):
            self.values.append([0] * y)

    def print(self):
        for x in range(self.x):
            for y in range(self.y - 1):
                print(self.values[x][y], end='\t')
            print(self.values[x][-1], end='\n')

    def fits(self, pallet, x, y):
        for i in range(pallet.x + 1):
            for j in range(pallet.y):
                if self.values[x + i - 1][y + j] != 0:
                    return False
        for pillar in self.pillars:
            # print(f"fit check: {pallet.num}")
            if (x < pillar[0] < pallet.x + x) and (y < pillar[1] < pallet.y + y):
                # print(f"at ({x}, {y}), pillar:({pillar[0], pillar[1]}), pallet{pallet.num}: ({pallet.x}, {pallet.y})")
                return False
        return True

    def count_fitting_places(self, pallet):
        count = 0
        for x in range(self.x - pallet.x + 1):
            # print(f"{pallet.num} ({pallet.x}, {pallet.y})")
            for y in range(self.y - pallet.y + 1):
                # print(f"{pallet.num}, {x}, {y}")
                if self.fits(pallet, x, y):
                    count += 1
        if pallet.x == pallet.y:
            pallet.fittingPos = count
            return
        pallet.rotate()
        for x in range(self.x - pallet.x):
            for y in range(self.y - pallet.y):
                if self.fits(pallet, x, y):
                    count += 1
        pallet.fittingPos = count
        # print(f"{pallet.x}, {pallet.y}: {pallet.fittingPos}")

    def remove_pallet(self, pallet):
        for x in range(self.x):
            for y in range(self.y):
                if self.values[x][y] == pallet.num:
                    self.values[x][y] = 0

    def insert_pallet(self, pallet, x, y):
        for i in range(pallet.x):
            for j in range(pallet.y):
                self.values[x + i][y + j] = pallet.num


class Pallet:
    def __init__(self, coords, num):
        self.x = coords[1]
        self.y = coords[0]
        self.num = num
        self.fittingPos = None

    def rotate(self):
        temp = self.x
        self.x = self.y
        self.y = temp


def metric(e):
    return e.fittingPos


def process(ware_house, pallets):
    print(pallets[0].num)
    if len(pallets) == 0:
        return True
    for pal in pallets:  # kiszámolom a pillarokra, hány helyen lehetnek
        ware_house.count_fitting_places(pal)
    pallets.sort(key=metric)  # rendezem őket e szerint növekvő sorrendbe

    this_pallet = pallets[0]
    if this_pallet.fittingPos == 0:
        return False
    pallets.remove(this_pallet)
    for x in range(ware_house.x - this_pallet.x):
        for y in range(ware_house.y - this_pallet.y):
            if warehouse.fits(this_pallet, x, y):
                ware_house.insert_pallet(this_pallet, x, y)
                #print(f"Inserted pallet #{this_pallet.num}({this_pallet.x}, {this_pallet.y}) at position ({x}, {y})")
                if process(ware_house, pallets):
                    return True
    this_pallet.rotate()
    for x in range(ware_house.x - this_pallet.x):
        for y in range(ware_house.y - this_pallet.y):
            if warehouse.fits(this_pallet, x, y):
                ware_house.insert_pallet(this_pallet, x, y)
                #print(f"Inserted pallet #{this_pallet.num}({this_pallet.x}, {this_pallet.y}) at position ({x}, {y})")
                if process(ware_house, pallets):
                    return True
    #print(f"{this_pallet.num}")


def read_all():
    f = open('demo.txt', 'rt')  # sys.stdin
    storage_area = [int(i) for i in f.readline().rstrip().split("\t")]
    number_of_columns = int(f.readline().rstrip())
    number_of_pallets = int(f.readline().rstrip())
    list_of_pillars = []
    list_of_pallets = []
    for i in range(number_of_columns):
        list_of_pillars.append([int(j) - 1 for j in f.readline().rstrip().split("\t")])
    for i in range(number_of_pallets):
        list_of_pallets.append(Pallet([int(j) for j in f.readline().rstrip().split("\t")], i + 1))
    return Warehouse(storage_area[0], storage_area[1], list_of_pillars), list_of_pallets


if __name__ == '__main__':
    warehouse, all_pallets = read_all()
    print(process(warehouse, all_pallets))
    warehouse.print()







