from data.cdn.sof_cdn import CoreTagClfCache

if __name__ == '__main__':
    core_clf = CoreTagClfCache.get()
    core_clf['ruby'] = core_clf.pop('ruby-on-rails')
    CoreTagClfCache.set(core_clf)