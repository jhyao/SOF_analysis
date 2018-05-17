from data.cache.sof_cache import CoreTagClfCache

if __name__ == '__main__':
    data = CoreTagClfCache.get()
    data.pop('others', [])
    CoreTagClfCache.set(data)