class HashSet:
    def info(self):
        s = '['
        for x in self:
            s += repr(x) + ', '

        if (len(s) > 2):
            s = s[:-2] + ']'
        else:
            s += ']'
        print(s)

    def __str__(self):
        lst = []
        for x in self:
            lst.append(x)

        lst = sorted(lst)

        return str(lst)

    def __len__(self):
        return self.numItems

    def __iter__(self):
        for i in range(len(self.items)):
            if self.items[i] != None and type(self.items[i]) != HashSet.__Placeholder:
                yield self.items[i]

                # 初始化

    def __init__(self, contents=[]):
        self.items = [None] * 10
        self.numItems = 0

        for item in contents:
            self.add(item)

    def __add(item, items):
        idx = hash(item) % len(items)
        loc = -1

        while items[idx] != None:
            if items[idx] == item:
                # item already in set
                return False

            if loc < 0 and type(items[idx]) == HashSet.__Placeholder:
                loc = idx

            idx = (idx + 1) % len(items)

        if loc < 0:
            loc = idx

        items[loc] = item
        return True

    def __rehash(oldList, newList):
        for x in oldList:
            if x != None and type(x) != HashSet.__Placeholder:
                HashSet.__add(x, newList)

        return newList

    def add(self, item):
        if HashSet.__add(item, self.items):
            self.numItems += 1
            load = self.numItems / len(self.items)
            if load >= 0.75:
                self.items = HashSet.__rehash(self.items, [None] * 2 * len(self.items))

    class __Placeholder:
        def __init__(self):
            pass

        def __eq__(self, other):
            return False

    def __remove(item, items):
        idx = hash(item) % len(items)

        while items[idx] != None:
            if items[idx] == item:
                nextIdx = (idx + 1) % len(items)
                if items[nextIdx] == None:
                    items[idx] = None
                else:
                    items[idx] = HashSet.__Placeholder()
                return True

            idx = (idx + 1) % len(items)

        return False

    def remove(self, item):
        if HashSet.__remove(item, self.items):
            self.numItems -= 1
            load = max(self.numItems, 10) / len(self.items)
            if load <= 0.25:
                self.items = HashSet.__rehash(self.items, [None] * int(len(self.items) / 2))
        else:
            raise KeyError("Item not in HashSet")

            # 任意弹出一个元素

    def pop(self):
        for x in self:
            self.remove(x)
            return x

            # discard和remove的区别在于，如果删除的元素不存在，也不抛出异常

    def discard(self, item):
        if HashSet.__remove(item, self.items):
            self.numItems -= 1
            load = max(self.numItems, 10) / len(self.items)
            if load <= 0.25:
                self.items = HashSet.__rehash(self.items, [None] * int(len(self.items) / 2))

    def __contains__(self, item):
        idx = hash(item) % len(self.items)
        while self.items[idx] != None:
            if self.items[idx] == item:
                return True

            idx = (idx + 1) % len(self.items)

        return False

        # 两个集合没有相同元素返回真

    def isdisjoint(self, t):
        for x in self:
            if x in t:
                return False

        return True

        # s是不是t的子集

    def issubset(self, t):
        for x in self:
            if x not in t:
                return False

        return True

        # s是不是t的超集

    def issuperset(self, t):
        for x in t:
            if x not in self:
                return False

        return True

        # 并集

    def union(self, t):
        result = HashSet(self)
        for x in t:
            result.add(x)

        return result

    def update(self, t):
        for x in t:
            self.add(x)

            # 交集

    def intersection_update(self, other):
        for item in self:
            if item not in other:
                self.discard(item)

    def intersection(self, other):
        result = HashSet(self)
        result.intersection_update(other)
        return result

        # 并集减去交集

    def symmetric_difference_update(self, other):
        I = self.intersection(other)
        self.difference_update(I)
        for x in other:
            if x not in I:
                self.add(x)

    def symmetric_difference(self, other):
        result = HashSet(self)
        result.symmetric_difference_update(other)
        return result

        # 差集

    def difference_update(self, other):
        for item in other:
            self.discard(item)

    def difference(self, other):
        result = HashSet(self)
        result.difference_update(other)
        return result

        # 浅拷贝

    def copy(self):
        return self

        # One extra HashSet method for use with the HashMap class.

    def __getitem__(self, item):
        idx = hash(item) % len(self.items)
        while self.items[idx] != None:
            if self.items[idx] == item:
                return self.items[idx]

            idx = (idx + 1) % len(self.items)

        return None

    def __repr__(self):
        s = 'HashSet(['
        for x in self:
            s += repr(x) + ', '

        if (len(s) > 2):
            s = s[:-2] + '])'
        else:
            s += '])'

        return s