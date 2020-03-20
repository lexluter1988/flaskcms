from abc import ABC, abstractmethod


class AbsTask(ABC):
    @abstractmethod
    def execute(self):
        raise NotImplemented

    @abstractmethod
    def rollback(self):
        raise NotImplemented


class AbsPipeline(ABC):
    @abstractmethod
    def task_add(self, config):
        raise NotImplemented

    @abstractmethod
    def task_remove(self, config):
        raise NotImplemented

    @abstractmethod
    def run_pipeline(self):
        raise NotImplemented


class AbsBuilder(ABC):
    @abstractmethod
    def pipeline_add(self, config):
        raise NotImplemented

    @abstractmethod
    def pipeline_remove(self, config):
        raise NotImplemented

    @abstractmethod
    def build(self, config):
        raise NotImplemented
