from pathlib import Path, PurePath, PureWindowsPath, PosixPath, PurePosixPath

# p = Path('.')
# print([x for x in p.iterdir()])

pp = PurePath('c:/a//b') / '2'
ppa = Path('c:/a/b')

ppa.exists()
print([x for x in pp.parents])
print(Path('c:/a//b') / 'c')
print(PureWindowsPath('c:/a/b') / 'd')

print(PurePath('/abc\\2.txt').as_posix())
print(PurePath('a/b/c').with_name('d.txt'))
