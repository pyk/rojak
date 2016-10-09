package com.rojak.rojakandroid.di.component;

import com.rojak.rojakandroid.RojakBaseApplication;
import com.rojak.rojakandroid.data.local.PreferencesHelper;
import com.rojak.rojakandroid.data.remote.APIService;
import com.rojak.rojakandroid.data.remote.UnauthorisedInterceptor;
import com.rojak.rojakandroid.di.module.ApplicationModule;

import org.greenrobot.eventbus.EventBus;

import javax.inject.Singleton;

import dagger.Component;

@Singleton
@Component(modules = {ApplicationModule.class})
public interface ApplicationComponent {

    void inject(RojakBaseApplication baseApplication);

    void inject(UnauthorisedInterceptor unauthorisedInterceptor);

    APIService apiService();

    EventBus eventBus();

    PreferencesHelper prefsHelper();

}