package com.rojak.rojakandroid.di.component;

import com.rojak.rojakandroid.RojakBaseApplication;
import com.rojak.rojakandroid.di.ActivityScope;

import dagger.Component;

@ActivityScope
@Component(dependencies = ApplicationComponent.class)
public interface ActivityComponent extends ApplicationComponent {
    void inject(RojakBaseApplication baseActivity);
}