package com.rojak.rojakandroid;

import android.app.Application;
import android.content.Context;
import android.content.pm.ApplicationInfo;
import android.support.annotation.VisibleForTesting;

import com.rojak.rojakandroid.di.component.ApplicationComponent;
import com.rojak.rojakandroid.di.component.DaggerApplicationComponent;
import com.rojak.rojakandroid.di.module.ApplicationModule;
import com.rojak.rojakandroid.events.AuthenticationErrorEvent;

import org.greenrobot.eventbus.EventBus;
import org.greenrobot.eventbus.Subscribe;

import javax.inject.Inject;

import rx.Scheduler;
import rx.schedulers.Schedulers;
import timber.log.Timber;

/**
 * Created on : October/09/2016
 * Author     : mnafian
 * Company    : PixilApps
 * Project    : RojakAndroid
 */

public class RojakBaseApplication extends Application {
    @Inject
    EventBus mEventBus;
    private Scheduler mScheduler;
    private ApplicationComponent mApplicationComponent;

    public static RojakBaseApplication get(Context context) {
        return (RojakBaseApplication) context.getApplicationContext();
    }

    @Override
    public void onCreate() {
        super.onCreate();

        boolean isDebuggable = (0 != (getApplicationInfo().flags & ApplicationInfo.FLAG_DEBUGGABLE));

        if (isDebuggable) {
            Timber.plant(new Timber.DebugTree());
        }

        mApplicationComponent = DaggerApplicationComponent.builder().applicationModule(new ApplicationModule(this)).build();

        mApplicationComponent.inject(this);
        mEventBus.register(this);
    }

    public ApplicationComponent getApplicationComponent() {
        return mApplicationComponent;
    }

    @VisibleForTesting
    public void setApplicationComponent(ApplicationComponent applicationComponent) {
        this.mApplicationComponent = applicationComponent;
    }

    public Scheduler getSubscribeScheduler() {
        if (mScheduler == null) {
            mScheduler = Schedulers.io();
        }
        return mScheduler;
    }

    @Override
    public void onLowMemory() {
        super.onLowMemory();
        Timber.e("########## onLowMemory ##########");
    }

    @Override
    public void onTerminate() {
        mEventBus.unregister(this);
        super.onTerminate();
    }

    @Subscribe
    public void onEvent(AuthenticationErrorEvent event) {
        Timber.e("Unauthorized! Redirect to Signin Activity..!.");
    }

}
