package id.artificialintelligence.rojak.di.component;

import id.artificialintelligence.rojak.RojakBaseApplication;
import id.artificialintelligence.rojak.di.ActivityScope;

import dagger.Component;

@ActivityScope
@Component(dependencies = ApplicationComponent.class)
public interface ActivityComponent extends ApplicationComponent {
    void inject(RojakBaseApplication baseActivity);
}